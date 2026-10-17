package com.restartday.fitness.app;

import android.content.Context;

import java.security.KeyStore;

/** Remove the former private-update credential without touching fitness or AI settings. */
final class LegacyUpdateCredentials {
    private LegacyUpdateCredentials() { }

    static void clear(Context context) {
        context.deleteSharedPreferences("github_updates");
        try {
            KeyStore store = KeyStore.getInstance("AndroidKeyStore");
            store.load(null);
            if (store.containsAlias("fitness_github_update_token_v1")) {
                store.deleteEntry("fitness_github_update_token_v1");
            }
        } catch (Exception ignored) {
            // Public updates work independently of the retired credential.
        }
    }
}
