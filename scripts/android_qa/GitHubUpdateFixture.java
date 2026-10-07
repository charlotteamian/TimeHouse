package com.restartday.fitness.qa;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.ParcelFileDescriptor;

import org.json.JSONObject;

import java.io.File;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

/** Emulator-only integration fixture. The temporary API token is deleted before use. */
public final class GitHubUpdateFixture extends Instrumentation {
    private String mode;

    @Override public void onCreate(Bundle arguments) {
        super.onCreate(arguments);
        mode = arguments == null ? "download" : arguments.getString("mode", "download");
        start();
    }

    private static Object field(Object object, String name) throws Exception {
        Field field = object.getClass().getDeclaredField(name);
        field.setAccessible(true);
        return field.get(object);
    }

    private static Method method(Class<?> type, String name, Class<?>... arguments) throws Exception {
        Method method = type.getDeclaredMethod(name, arguments);
        method.setAccessible(true);
        return method;
    }

    @Override public void onStart() {
        Bundle result = new Bundle();
        Context context = getTargetContext();
        File tokenFile = new File(context.getCacheDir(), ".github-qa-token");
        try {
            if (!"com.restartday.fitness".equals(context.getPackageName())) throw new AssertionError("Wrong target package");
            ClassLoader loader = context.getClassLoader();
            Class<?> clientType = loader.loadClass("com.restartday.fitness.app.GitHubUpdater");
            Class<?> releaseType = loader.loadClass("com.restartday.fitness.app.GitHubUpdater$Release");
            File verified = new File(context.getCacheDir(), "updates/qa-verified.json");
            File apk = new File(context.getCacheDir(), "updates/timehouse-debug.apk");
            if ("installer".equals(mode)) {
                JSONObject metadata = new JSONObject(Files.readString(verified.toPath()));
                Constructor<?> constructor = releaseType.getDeclaredConstructor(long.class, String.class, long.class, String.class, long.class);
                constructor.setAccessible(true);
                Object release = constructor.newInstance(metadata.getLong("version_code"), metadata.getString("version_name"),
                        metadata.getLong("bytes"), metadata.getString("sha256"), metadata.getLong("asset"));
                method(clientType, "verifyPackage", Context.class, File.class, releaseType).invoke(null, context, apk, release);
                Activity activity = startActivitySync(new Intent().setClassName(context.getPackageName(),
                        "com.restartday.fitness.app.MainActivity").addFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
                Method launch = method(activity.getClass(), "launchUpdateInstaller", File.class);
                runOnMainSync(() -> {
                    try { launch.invoke(activity, apk); }
                    catch (Exception error) { throw new RuntimeException(error); }
                });
                result.putString("result", "Verified APK passed to installation flow");
                finish(Activity.RESULT_OK, result);
                return;
            }
            String token = Files.readString(tokenFile.toPath(), StandardCharsets.UTF_8).trim();
            if (!tokenFile.delete()) throw new AssertionError("Temporary token was not deleted");
            Constructor<?> constructor = clientType.getDeclaredConstructor();
            constructor.setAccessible(true);
            Object client = constructor.newInstance();
            Class<?> checkType = loader.loadClass("com.restartday.fitness.app.GitHubUpdater$CheckCallback");
            AtomicReference<Object> release = new AtomicReference<>();
            AtomicReference<String> failure = new AtomicReference<>();
            CountDownLatch checked = new CountDownLatch(1);
            Object checkCallback = Proxy.newProxyInstance(loader, new Class<?>[]{checkType}, (proxy, called, values) -> {
                if ("onRelease".equals(called.getName())) release.set(values[0]);
                else if ("onError".equals(called.getName())) failure.set((String) values[0]);
                checked.countDown();
                return null;
            });
            method(clientType, "check", String.class, checkType).invoke(client, token, checkCallback);
            if (!checked.await(60, TimeUnit.SECONDS) || failure.get() != null || release.get() == null) {
                throw new AssertionError(failure.get() == null ? "Release lookup timed out" : failure.get());
            }
            Object found = release.get();
            long code = (Long) field(found, "versionCode");
            result.putLong("version_code", code);
            result.putString("version_name", (String) field(found, "versionName"));
            Bundle status = new Bundle(); status.putString("phase", "Private release lookup passed"); sendStatus(1, status);
            Class<?> downloadType = loader.loadClass("com.restartday.fitness.app.GitHubUpdater$DownloadCallback");
            CountDownLatch downloaded = new CountDownLatch(1);
            AtomicReference<File> ready = new AtomicReference<>();
            int[] lastStep = {-1};
            File orphan = new File(apk.getParentFile(), "download-qa-orphan.part");
            orphan.getParentFile().mkdirs();
            Files.write(orphan.toPath(), new byte[4096]);
            File live = new File(apk.getParentFile(), "download-qa-live.part");
            File concurrent = new File(apk.getParentFile(), "download-qa-concurrent.part");
            method(clientType, "preparePart", File.class).invoke(null, live);
            Files.write(live.toPath(), new byte[4096]);
            method(clientType, "preparePart", File.class).invoke(null, concurrent);
            if (!live.isFile() || orphan.exists()) throw new AssertionError("Partial cleanup did not preserve the active download");
            method(clientType, "finishPart", File.class).invoke(null, live);
            method(clientType, "finishPart", File.class).invoke(null, concurrent);
            Files.write(orphan.toPath(), new byte[4096]);
            Object downloadCallback = Proxy.newProxyInstance(loader, new Class<?>[]{downloadType}, (proxy, called, values) -> {
                if ("onReady".equals(called.getName())) { ready.set((File) values[0]); downloaded.countDown(); }
                else if ("onError".equals(called.getName())) { failure.set((String) values[0]); downloaded.countDown(); }
                else if ("onProgress".equals(called.getName())) {
                    int step = (int) (((Long) values[0]) * 5 / (Long) values[1]);
                    if (step != lastStep[0]) {
                        lastStep[0] = step;
                        Bundle progress = new Bundle(); progress.putInt("download_percent", step * 20); sendStatus(1, progress);
                    }
                }
                return null;
            });
            method(clientType, "download", Context.class, String.class, releaseType, downloadType)
                    .invoke(client, context, token, found, downloadCallback);
            if (!downloaded.await(12, TimeUnit.MINUTES) || ready.get() == null || failure.get() != null) {
                method(clientType, "cancel").invoke(client);
                throw new AssertionError(failure.get() == null ? "Download timed out" : failure.get());
            }
            Uri uri = Uri.parse("content://com.restartday.fitness.updates/timehouse-debug.apk");
            if (orphan.exists()) throw new AssertionError("Abandoned partial download was not removed");
            try (ParcelFileDescriptor descriptor = context.getContentResolver().openFileDescriptor(uri, "r")) {
                if (descriptor == null || descriptor.getStatSize() != ready.get().length()) throw new AssertionError("APK provider size mismatch");
            }
            boolean rejected = false;
            try (ParcelFileDescriptor ignored = context.getContentResolver().openFileDescriptor(uri, "w")) { }
            catch (SecurityException expected) { rejected = true; }
            if (!rejected) throw new AssertionError("Provider allowed writes");
            rejected = false;
            try { rejected = context.getContentResolver().getType(Uri.parse("content://com.restartday.fitness.updates/../files/secret")) == null; }
            catch (SecurityException expected) { rejected = true; }
            if (!rejected) throw new AssertionError("Provider allowed another path");
            Constructor<?> releaseConstructor = releaseType.getDeclaredConstructor(long.class, String.class, long.class, String.class, long.class);
            releaseConstructor.setAccessible(true);
            Object mismatched = releaseConstructor.newInstance(code, "incorrect-version", field(found, "bytes"),
                    field(found, "sha256"), field(found, "apkAssetId"));
            rejected = false;
            try { method(clientType, "verifyPackage", Context.class, File.class, releaseType).invoke(null, context, apk, mismatched); }
            catch (java.lang.reflect.InvocationTargetException expected) { rejected = true; }
            if (!rejected) throw new AssertionError("APK version name mismatch was accepted");
            JSONObject saved = new JSONObject();
            saved.put("version_code", code); saved.put("version_name", field(found, "versionName"));
            saved.put("bytes", field(found, "bytes")); saved.put("sha256", field(found, "sha256")); saved.put("asset", field(found, "apkAssetId"));
            Files.writeString(verified.toPath(), saved.toString());
            result.putLong("bytes", ready.get().length());
            result.putString("result", "Private lookup, download, SHA-256, version, signing identity and read-only APK provider passed");
            finish(Activity.RESULT_OK, result);
        } catch (Throwable error) {
            result.putString("failure", error.getClass().getSimpleName() + ": " + error.getMessage());
            finish(Activity.RESULT_CANCELED, result);
        } finally {
            tokenFile.delete();
        }
    }
}
