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
        check(GitHubUpdatePolicy.isReleaseApi(api), "Recognise this public release asset API");
        check(GitHubUpdatePolicy.isReleaseApi(URI.create("https://api.github.com/repos/charlotteamian/TimeHouse/releases/tags/latest-build")), "Recognise the fixed public release tag API");
        check(!GitHubUpdatePolicy.isReleaseApi(URI.create("https://api.github.com/repos/other/project/releases/assets/1")), "Do not apply repository API headers to another repository");
        check(!GitHubUpdatePolicy.isReleaseApi(URI.create("https://release-assets.githubusercontent.com/path?signature=test")), "Do not apply API headers to signed asset URLs");
        check(!GitHubUpdatePolicy.isTrustedDownload(URI.create("http://api.github.com/path")), "Reject cleartext redirects");
        check(!GitHubUpdatePolicy.isTrustedDownload(URI.create("https://api.github.com.evil.test/path")), "Reject lookalike hosts");
        check(!GitHubUpdatePolicy.isTrustedDownload(URI.create("https://api.github.com@evil.test/path")), "Reject userinfo tricks");
        check(!GitHubUpdatePolicy.isTrustedDownload(URI.create("https://api.github.com:8443/path")), "Reject alternate ports");
        check(GitHubUpdatePolicy.isTrustedDownload(URI.create("https://objects.githubusercontent.com/path")), "Allow GitHub asset CDN");
        check(GitHubUpdatePolicy.isTrustedDownload(URI.create("https://release-assets.githubusercontent.com/path?signature=test")), "Allow signed release asset redirects");
        check(GitHubUpdatePolicy.isTrustedDownload(URI.create("https://github.com/charlotteamian/TimeHouse/releases/download/latest-build/update.json")), "Allow public browser asset redirects");
        check(!GitHubUpdatePolicy.isTrustedDownload(URI.create("https://evil.test/path")), "Reject untrusted HTTPS hosts");
        check(!GitHubUpdatePolicy.isReleaseApi(URI.create("https://api.github.com/repos/charlotteamian/TimeHouse/releases-other/assets/1")), "Do not recognise lookalike API paths");
        check(GitHubUpdatePolicy.httpError(404, null, null).contains("公开版本"), "Explain a missing public release without requesting credentials");
        check(GitHubUpdatePolicy.httpError(429, null, null).contains("过于频繁"), "Explain a public request rate limit");
        check(GitHubUpdatePolicy.httpError(403, "0", null).contains("过于频繁"), "Recognise exhausted anonymous API quota");
        check(GitHubUpdatePolicy.httpError(403, "55", "60").contains("过于频繁"), "Recognise secondary rate limits");
        check(GitHubUpdatePolicy.httpError(403, "55", null).contains("（403）"), "Report a forbidden public request as a service error");
        check(GitHubUpdatePolicy.httpError(401, "0", null).contains("（401）"), "Report unexpected public authentication requirements as a service error");
        check(GitHubUpdatePolicy.httpError(500, "0", null).contains("（500）"), "Do not hide server errors behind quota headers");
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
