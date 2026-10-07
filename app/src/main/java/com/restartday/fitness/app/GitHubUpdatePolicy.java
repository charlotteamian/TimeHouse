package com.restartday.fitness.app;

import java.net.URI;
import java.security.MessageDigest;
import java.util.HashSet;
import java.util.Set;

/** Update checks shared by the network client and the plain Java tests. */
final class GitHubUpdatePolicy {
    static final String REPOSITORY = "charlotteamian/TimeHouse";
    static final String PACKAGE_NAME = "com.restartday.fitness";
    static final String APK_NAME = "timehouse-debug.apk";
    static final String API_PREFIX = "/repos/" + REPOSITORY + "/releases/";
    static final long MAX_APK_BYTES = 1024L * 1024 * 1024;

    private GitHubUpdatePolicy() {}

    static boolean isNewer(long remoteCode, long installedCode) {
        return remoteCode > installedCode && remoteCode <= 2100000000L;
    }

    static boolean isTrustedDownload(URI uri) {
        if (uri == null || !"https".equalsIgnoreCase(uri.getScheme())
                || uri.getUserInfo() != null || (uri.getPort() != -1 && uri.getPort() != 443)) return false;
        String host = uri.getHost();
        return "api.github.com".equalsIgnoreCase(host) || "github.com".equalsIgnoreCase(host)
                || "release-assets.githubusercontent.com".equalsIgnoreCase(host)
                || "objects.githubusercontent.com".equalsIgnoreCase(host);
    }

    static boolean maySendToken(URI uri) {
        return isTrustedDownload(uri) && "api.github.com".equalsIgnoreCase(uri.getHost())
                && uri.getPath() != null && uri.getPath().startsWith(API_PREFIX);
    }

    static void validateMetadata(String packageName, long versionCode, String versionName,
            long bytes, String sha256) {
        if (!PACKAGE_NAME.equals(packageName) || versionCode <= 0 || versionCode > 2100000000L
                || versionName == null || versionName.trim().isEmpty() || versionName.length() > 80
                || bytes <= 0 || bytes > MAX_APK_BYTES || sha256 == null
                || !sha256.matches("[0-9a-fA-F]{64}")) {
            throw new IllegalArgumentException("Invalid update metadata");
        }
    }

    static boolean sameSigners(byte[][] installed, byte[][] downloaded) {
        if (installed == null || downloaded == null || installed.length == 0 || downloaded.length == 0) return false;
        return signerHashes(installed).equals(signerHashes(downloaded));
    }

    private static Set<String> signerHashes(byte[][] signers) {
        Set<String> result = new HashSet<String>();
        for (byte[] signer : signers) result.add(hex(digest(signer)));
        return result;
    }

    static byte[] digest(byte[] value) {
        try {
            return MessageDigest.getInstance("SHA-256").digest(value);
        } catch (Exception error) {
            throw new IllegalStateException(error);
        }
    }

    static String hex(byte[] value) {
        StringBuilder result = new StringBuilder(value.length * 2);
        for (byte b : value) result.append(String.format(java.util.Locale.ROOT, "%02x", b & 0xff));
        return result.toString();
    }
}
