package com.restartday.fitness.app;

import java.net.URI;

public final class GitHubUpdatePolicyTest {
    private static int checks;

    private static void check(boolean value, String message) {
        checks++;
        if (!value) throw new AssertionError(message);
    }

    private static void reject(String pkg, long code, String version, long bytes, String sha) {
        boolean rejected = false;
        try { GitHubUpdatePolicy.validateMetadata(pkg, code, version, bytes, sha); }
        catch (IllegalArgumentException expected) { rejected = true; }
        check(rejected, "Invalid metadata must be rejected");
    }

    public static void main(String[] args) {
        check(GitHubUpdatePolicy.isNewer(2026100701L, 2026091901L), "Compare numeric version codes");
        check(!GitHubUpdatePolicy.isNewer(2026100701L, 2026100701L), "Do not reinstall the same build");
        check(!GitHubUpdatePolicy.isNewer(2026091901L, 2026100701L), "Do not downgrade");
        check(!GitHubUpdatePolicy.isNewer(Long.MAX_VALUE, 1), "Reject version overflow");
        URI api = URI.create("https://api.github.com/repos/charlotteamian/TimeHouse/releases/assets/123");
        check(GitHubUpdatePolicy.maySendToken(api), "Authenticate this repository API");
        check(!GitHubUpdatePolicy.maySendToken(URI.create("https://api.github.com/repos/other/project/releases/assets/1")), "Do not send token to another repository");
        check(!GitHubUpdatePolicy.maySendToken(URI.create("https://release-assets.githubusercontent.com/path?signature=test")), "Do not forward token to signed asset URLs");
        check(!GitHubUpdatePolicy.isTrustedDownload(URI.create("http://api.github.com/path")), "Reject cleartext redirects");
        check(!GitHubUpdatePolicy.isTrustedDownload(URI.create("https://api.github.com.evil.test/path")), "Reject lookalike hosts");
        check(!GitHubUpdatePolicy.isTrustedDownload(URI.create("https://api.github.com@evil.test/path")), "Reject userinfo tricks");
        check(!GitHubUpdatePolicy.isTrustedDownload(URI.create("https://api.github.com:8443/path")), "Reject alternate ports");
        check(GitHubUpdatePolicy.isTrustedDownload(URI.create("https://objects.githubusercontent.com/path")), "Allow GitHub asset CDN");
        String sha = "a".repeat(64);
        GitHubUpdatePolicy.validateMetadata(GitHubUpdatePolicy.PACKAGE_NAME, 2026100701L, "1.2.17", 480000000L, sha);
        check(true, "Accept valid release metadata");
        reject("other.app", 2026100701L, "1.2.17", 480000000L, sha);
        reject(GitHubUpdatePolicy.PACKAGE_NAME, 0, "1.2.17", 480000000L, sha);
        reject(GitHubUpdatePolicy.PACKAGE_NAME, 2026100701L, "", 480000000L, sha);
        reject(GitHubUpdatePolicy.PACKAGE_NAME, 2026100701L, "1.2.17", 0, sha);
        reject(GitHubUpdatePolicy.PACKAGE_NAME, 2026100701L, "1.2.17", Long.MAX_VALUE, sha);
        reject(GitHubUpdatePolicy.PACKAGE_NAME, 2026100701L, "1.2.17", 480000000L, "not-a-hash");
        byte[][] current = {{1, 2, 3}};
        check(GitHubUpdatePolicy.sameSigners(current, new byte[][]{{1, 2, 3}}), "Accept original signing identity");
        check(!GitHubUpdatePolicy.sameSigners(current, new byte[][]{{1, 2, 4}}), "Reject another signing identity");
        check(!GitHubUpdatePolicy.sameSigners(current, null), "Reject missing signatures");
        check(!GitHubUpdatePolicy.sameSigners(new byte[0][], new byte[0][]), "Reject empty signer sets");
        check(GitHubUpdatePolicy.hex(GitHubUpdatePolicy.digest("abc".getBytes(java.nio.charset.StandardCharsets.UTF_8)))
                .equals("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"), "Use SHA-256");
        System.out.println("GitHubUpdatePolicyTest: " + checks + " checks passed");
    }
}
