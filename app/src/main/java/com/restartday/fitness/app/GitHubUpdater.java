package com.restartday.fitness.app;

import android.content.Context;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.content.pm.Signature;
import android.os.Handler;
import android.os.Looper;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.atomic.AtomicBoolean;

/** Authenticated private Release downloads with size, hash, version and signer checks. */
final class GitHubUpdater {
    static final class Release {
        final long versionCode;
        final String versionName;
        final long bytes;
        final String sha256;
        final long apkAssetId;

        Release(long code, String name, long size, String sha, long asset) {
            versionCode = code; versionName = name; bytes = size; sha256 = sha; apkAssetId = asset;
        }
    }

    interface CheckCallback {
        void onRelease(Release release);
        void onError(String message);
    }

    interface DownloadCallback {
        void onProgress(long bytes, long total);
        void onReady(File apk);
        void onError(String message);
    }

    private static final class UpdateException extends IOException {
        UpdateException(String message) { super(message); }
    }

    private static final class Task {
        final AtomicBoolean cancelled = new AtomicBoolean();
        volatile HttpURLConnection connection;
        void checkCancelled() throws IOException {
            if (cancelled.get()) throw new IOException("Cancelled");
        }
    }

    private final Handler main = new Handler(Looper.getMainLooper());
    private static final Set<File> activeParts = new HashSet<>();
    private Task current;

    private static synchronized void preparePart(File part) throws IOException {
        // Process death skips finally. Keep other live downloads, but reclaim
        // abandoned partial packages before checking available storage.
        File[] leftovers = part.getParentFile().listFiles();
        if (leftovers != null) for (File file : leftovers) {
            if (file.getName().startsWith("download-") && file.getName().endsWith(".part")
                    && file.isFile() && !activeParts.contains(file) && !file.delete()) {
                throw new UpdateException("无法清理中断的下载，请清理应用缓存后重试");
            }
        }
        activeParts.add(part);
    }

    private static synchronized void finishPart(File part) {
        if (part.exists()) part.delete();
        activeParts.remove(part);
    }

    synchronized void cancel() {
        if (current == null) return;
        current.cancelled.set(true);
        if (current.connection != null) current.connection.disconnect();
    }

    private synchronized Task begin() {
        cancel();
        current = new Task();
        return current;
    }

    private void post(Task task, Runnable action) {
        if (!task.cancelled.get()) main.post(() -> { if (!task.cancelled.get()) action.run(); });
    }

    void check(String token, CheckCallback callback) {
        Task task = begin();
        new Thread(() -> {
            try {
                JSONObject release = json(task, api("tags/latest-build"), token, false);
                if (release.optBoolean("draft") || !"latest-build".equals(release.optString("tag_name"))) {
                    throw new UpdateException("新版本尚未发布，请稍后再试");
                }
                JSONArray assets = release.getJSONArray("assets");
                JSONObject apk = asset(assets, GitHubUpdatePolicy.APK_NAME);
                JSONObject metadataAsset = asset(assets, "update.json");
                JSONObject metadata = json(task, api("assets/" + metadataAsset.getLong("id")), token, true);
                if (metadata.getInt("format_version") != 1 || !GitHubUpdatePolicy.APK_NAME.equals(metadata.getString("apk_name"))) {
                    throw new UpdateException("版本信息格式不支持，请联系项目维护者");
                }
                long code = metadata.getLong("version_code");
                String name = metadata.getString("version_name");
                long bytes = metadata.getLong("apk_bytes");
                String hash = metadata.getString("apk_sha256");
                GitHubUpdatePolicy.validateMetadata(metadata.getString("package_name"), code, name, bytes, hash);
                long assetId = apk.getLong("id");
                if (assetId <= 0 || metadata.getLong("apk_asset_id") != assetId || apk.getLong("size") != bytes) {
                    throw new UpdateException("新版本正在发布，请稍后重新检查");
                }
                Release found = new Release(code, name, bytes, hash, assetId);
                post(task, () -> callback.onRelease(found));
            } catch (Exception error) {
                post(task, () -> callback.onError(describe(error)));
            }
        }, "github-update-check").start();
    }

    void download(Context context, String token, Release release, DownloadCallback callback) {
        Task task = begin();
        Context app = context.getApplicationContext();
        new Thread(() -> {
            File apk = UpdateApkProvider.apkFile(app);
            File part = new File(apk.getParentFile(), "download-" + System.nanoTime() + ".part");
            try {
                if (!apk.getParentFile().isDirectory() && !apk.getParentFile().mkdirs()) {
                    throw new UpdateException("无法创建下载目录，请检查手机存储空间");
                }
                task.checkCancelled();
                preparePart(part);
                if (apk.isFile() && apk.length() == release.bytes && checksum(task, apk).equalsIgnoreCase(release.sha256)) {
                    verifyPackage(app, apk, release);
                    post(task, () -> callback.onReady(apk));
                    return;
                }
                // A stale package may occupy the space needed for its replacement.
                if (apk.exists() && !apk.delete()) throw new UpdateException("无法清理旧安装包，请重试");
                if (apk.getParentFile().getUsableSpace() < release.bytes * 2 + 64L * 1024 * 1024) {
                    throw new UpdateException("手机空间不足，请至少预留 " + ((release.bytes * 2) / 1024 / 1024 + 64) + " MB 后重试");
                }
                HttpURLConnection connection = connect(task, api("assets/" + release.apkAssetId), token, true);
                long length = connection.getContentLengthLong();
                MessageDigest digest = MessageDigest.getInstance("SHA-256");
                long readBytes = 0;
                long lastProgress = 0;
                try {
                    if (length >= 0 && length != release.bytes) throw new UpdateException("安装包大小与版本信息不一致，请重新检查更新");
                    try (InputStream input = connection.getInputStream(); FileOutputStream output = new FileOutputStream(part)) {
                        byte[] buffer = new byte[65536];
                        int count;
                        while ((count = input.read(buffer)) != -1) {
                            task.checkCancelled();
                            readBytes += count;
                            if (readBytes > release.bytes) throw new UpdateException("安装包超出预期大小，已停止下载");
                            output.write(buffer, 0, count);
                            digest.update(buffer, 0, count);
                            long now = System.nanoTime();
                            if (now - lastProgress > 250000000L || readBytes == release.bytes) {
                                final long progress = readBytes;
                                post(task, () -> callback.onProgress(progress, release.bytes));
                                lastProgress = now;
                            }
                        }
                    }
                } finally {
                    connection.disconnect();
                }
                task.checkCancelled();
                if (readBytes != release.bytes || !GitHubUpdatePolicy.hex(digest.digest()).equalsIgnoreCase(release.sha256)) {
                    throw new UpdateException("下载包不完整或校验失败，请重新下载");
                }
                verifyPackage(app, part, release);
                task.checkCancelled();
                if (!part.renameTo(apk)) throw new UpdateException("无法保存安装包，请重试");
                post(task, () -> callback.onReady(apk));
            } catch (Exception error) {
                post(task, () -> callback.onError(describe(error)));
            } finally {
                finishPart(part);
            }
        }, "github-update-download").start();
    }

    private static byte[][] signers(PackageInfo info) {
        if (info == null || info.signingInfo == null) return null;
        Signature[] signatures = info.signingInfo.getApkContentsSigners();
        byte[][] result = new byte[signatures.length][];
        for (int i = 0; i < signatures.length; i++) result[i] = signatures[i].toByteArray();
        return result;
    }

    private static void verifyPackage(Context context, File file, Release release) throws Exception {
        PackageManager manager = context.getPackageManager();
        PackageInfo installed = manager.getPackageInfo(context.getPackageName(), PackageManager.GET_SIGNING_CERTIFICATES);
        PackageInfo downloaded = manager.getPackageArchiveInfo(file.getAbsolutePath(), PackageManager.GET_SIGNING_CERTIFICATES);
        if (downloaded == null || !context.getPackageName().equals(downloaded.packageName)
                || downloaded.getLongVersionCode() != release.versionCode
                || !release.versionName.equals(downloaded.versionName)
                || !GitHubUpdatePolicy.isNewer(downloaded.getLongVersionCode(), installed.getLongVersionCode())) {
            throw new UpdateException("安装包版本或包名不匹配，已停止安装");
        }
        if (!GitHubUpdatePolicy.sameSigners(signers(installed), signers(downloaded))) {
            throw new UpdateException("安装包签名与当前应用不同，已停止安装");
        }
    }

    private static String checksum(Task task, File file) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        try (InputStream input = new FileInputStream(file)) {
            byte[] buffer = new byte[65536];
            int count;
            while ((count = input.read(buffer)) != -1) {
                task.checkCancelled();
                digest.update(buffer, 0, count);
            }
        }
        return GitHubUpdatePolicy.hex(digest.digest());
    }

    private static JSONObject asset(JSONArray assets, String name) throws Exception {
        for (int i = 0; i < assets.length(); i++) {
            JSONObject asset = assets.getJSONObject(i);
            if (name.equals(asset.optString("name")) && "uploaded".equals(asset.optString("state"))) return asset;
        }
        throw new UpdateException("新版本安装包尚未就绪，请稍后重新检查");
    }

    private static URI api(String path) {
        return URI.create("https://api.github.com" + GitHubUpdatePolicy.API_PREFIX + path);
    }

    private JSONObject json(Task task, URI uri, String token, boolean binary) throws Exception {
        HttpURLConnection connection = connect(task, uri, token, binary);
        try (InputStream input = connection.getInputStream(); ByteArrayOutputStream output = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[8192];
            int count;
            while ((count = input.read(buffer)) != -1) {
                task.checkCancelled();
                output.write(buffer, 0, count);
                if (output.size() > 1024 * 1024) throw new UpdateException("版本信息过大，已停止请求");
            }
            return new JSONObject(new String(output.toByteArray(), StandardCharsets.UTF_8));
        } finally {
            connection.disconnect();
        }
    }

    private HttpURLConnection connect(Task task, URI uri, String token, boolean binary) throws Exception {
        URI currentUri = uri;
        for (int redirects = 0; redirects <= 5; redirects++) {
            task.checkCancelled();
            if (!GitHubUpdatePolicy.isTrustedDownload(currentUri)) throw new UpdateException("更新下载地址不可信，已停止请求");
            HttpURLConnection connection = (HttpURLConnection) currentUri.toURL().openConnection();
            task.connection = connection;
            connection.setInstanceFollowRedirects(false);
            connection.setConnectTimeout(15000);
            connection.setReadTimeout(45000);
            connection.setRequestProperty("Accept", binary ? "application/octet-stream" : "application/vnd.github+json");
            connection.setRequestProperty("User-Agent", "TimeHouse-Android-Updater");
            connection.setRequestProperty("Cache-Control", "no-cache");
            if (GitHubUpdatePolicy.maySendToken(currentUri)) {
                connection.setRequestProperty("Authorization", "Bearer " + token.trim());
                connection.setRequestProperty("X-GitHub-Api-Version", "2026-03-10");
            }
            int code;
            try {
                code = connection.getResponseCode();
            } catch (Exception error) {
                connection.disconnect();
                throw error;
            }
            if (code == 200) return connection;
            if (code == 301 || code == 302 || code == 303 || code == 307 || code == 308) {
                String location = connection.getHeaderField("Location");
                connection.disconnect();
                if (location == null) throw new UpdateException("GitHub 未提供下载地址，请稍后重试");
                currentUri = currentUri.resolve(location);
                continue;
            }
            String remaining = connection.getHeaderField("X-RateLimit-Remaining");
            connection.disconnect();
            if (code == 401 || (code == 403 && !"0".equals(remaining))) {
                throw new UpdateException("GitHub 令牌无效、已过期或没有读取权限，请重新配置");
            }
            if (code == 404) throw new UpdateException("未找到私有更新，请确认令牌已选择 TimeHouse 仓库及 Contents 只读权限");
            if (code == 429 || "0".equals(remaining)) throw new UpdateException("GitHub 请求过于频繁，请稍后重试");
            throw new UpdateException("GitHub 更新服务暂不可用（" + code + "），请稍后重试");
        }
        throw new UpdateException("下载重定向过多，请稍后重试");
    }

    private static String describe(Exception error) {
        if (error instanceof UpdateException) return error.getMessage();
        if (error instanceof org.json.JSONException || error instanceof IllegalArgumentException) {
            return "版本信息不完整，请稍后重新检查更新";
        }
        return "更新失败，请检查网络与手机存储空间后重试";
    }
}
