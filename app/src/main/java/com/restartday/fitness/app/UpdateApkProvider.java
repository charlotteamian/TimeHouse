package com.restartday.fitness.app;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.MatrixCursor;
import android.net.Uri;
import android.os.ParcelFileDescriptor;
import android.provider.OpenableColumns;

import java.io.File;
import java.io.FileNotFoundException;

/** Grants the package installer read access to exactly one verified APK. */
public final class UpdateApkProvider extends ContentProvider {
    private static final String AUTHORITY = "com.restartday.fitness.updates";
    private static final String PATH = "/" + GitHubUpdatePolicy.APK_NAME;

    static File apkFile(Context context) {
        return new File(new File(context.getCacheDir(), "updates"), GitHubUpdatePolicy.APK_NAME);
    }

    static Uri apkUri() {
        return new Uri.Builder().scheme("content").authority(AUTHORITY).path(PATH).build();
    }

    private File requireApk(Uri uri) {
        if (!AUTHORITY.equals(uri.getAuthority()) || !PATH.equals(uri.getPath())
                || uri.getQuery() != null || uri.getFragment() != null) {
            throw new SecurityException("Unsupported update URI");
        }
        return apkFile(getContext());
    }

    @Override public boolean onCreate() { return true; }

    @Override public String getType(Uri uri) {
        requireApk(uri);
        return "application/vnd.android.package-archive";
    }

    @Override public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException {
        if (!"r".equals(mode)) throw new SecurityException("Update APK is read-only");
        return ParcelFileDescriptor.open(requireApk(uri), ParcelFileDescriptor.MODE_READ_ONLY);
    }

    @Override public Cursor query(Uri uri, String[] projection, String selection,
            String[] selectionArgs, String sortOrder) {
        File file = requireApk(uri);
        String[] columns = projection == null
                ? new String[]{OpenableColumns.DISPLAY_NAME, OpenableColumns.SIZE} : projection;
        MatrixCursor cursor = new MatrixCursor(columns);
        Object[] row = new Object[columns.length];
        for (int i = 0; i < columns.length; i++) {
            if (OpenableColumns.DISPLAY_NAME.equals(columns[i])) row[i] = file.getName();
            else if (OpenableColumns.SIZE.equals(columns[i])) row[i] = file.length();
        }
        cursor.addRow(row);
        return cursor;
    }

    @Override public Uri insert(Uri uri, ContentValues values) { throw new UnsupportedOperationException(); }
    @Override public int update(Uri uri, ContentValues values, String selection, String[] args) { throw new UnsupportedOperationException(); }
    @Override public int delete(Uri uri, String selection, String[] args) { throw new UnsupportedOperationException(); }
}
