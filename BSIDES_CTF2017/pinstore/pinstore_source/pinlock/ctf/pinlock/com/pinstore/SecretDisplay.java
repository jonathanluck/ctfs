package pinlock.ctf.pinlock.com.pinstore;

import android.content.Context;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

public class SecretDisplay extends AppCompatActivity {
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView((int) C0175R.layout.activity_secret_display);
        Context context = getApplicationContext();
        TextView tv = (TextView) findViewById(C0175R.id.secretTextView);
        String pin = getIntent().getStringExtra("pin");
        try {
            tv.setText(new CryptoUtilities("v1", pin).decrypt(new DatabaseUtilities(getApplicationContext()).fetchSecret()));
        } catch (Exception e) {
            Log.e("Pinlock", "exception", e);
        }
        Toast toast = Toast.makeText(context, pin, 1);
    }
}
