package pinlock.ctf.pinlock.com.pinstore;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;
import android.support.v4.view.accessibility.AccessibilityNodeInfoCompat;
import android.util.Log;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

public class DatabaseUtilities extends SQLiteOpenHelper {
    private static String dbName;
    private static String pathToDB;
    private final Context appcontext;
    private SQLiteDatabase db;

    static {
        pathToDB = "/data/data/pinlock.ctf.pinlock.com.pinstore/databases/";
        dbName = "pinlock.db";
    }

    public DatabaseUtilities(Context context) throws IOException {
        super(context, dbName, null, 1);
        this.appcontext = context;
        createDB();
    }

    public String fetchSecret() throws IOException {
        openDB();
        Cursor cursor = this.db.rawQuery("SELECT entry FROM secretsDBv1", null);
        String secret = BuildConfig.FLAVOR;
        if (cursor.moveToFirst()) {
            secret = cursor.getString(0);
        }
        Log.d("secret", secret);
        cursor.close();
        return secret;
    }

    public String fetchPin() throws IOException {
        openDB();
        Cursor cursor = this.db.rawQuery("SELECT pin FROM pinDB", null);
        String pin = BuildConfig.FLAVOR;
        if (cursor.moveToFirst()) {
            pin = cursor.getString(0);
        }
        cursor.close();
        return pin;
    }

    public void createDB() throws IOException {
        SQLiteDatabase test = null;
        try {
            test = SQLiteDatabase.openDatabase(pathToDB + dbName, null, 1);
        } catch (SQLiteException e) {
        }
        if (test == null) {
            getReadableDatabase();
            InputStream input = this.appcontext.getAssets().open(dbName);
            OutputStream output = new FileOutputStream(pathToDB + dbName);
            byte[] buffer = new byte[AccessibilityNodeInfoCompat.ACTION_NEXT_HTML_ELEMENT];
            while (true) {
                int length = input.read(buffer);
                if (length > 0) {
                    output.write(buffer, 0, length);
                } else {
                    input.close();
                    output.flush();
                    output.close();
                    Log.d("DB", "created");
                    return;
                }
            }
        }
    }

    public void openDB() {
        this.db = SQLiteDatabase.openDatabase(pathToDB + dbName, null, 1);
    }

    public synchronized void close() {
        if (this.db != null) {
            this.db.close();
        }
        super.close();
    }

    public void onCreate(SQLiteDatabase db) {
    }

    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
    }
}
