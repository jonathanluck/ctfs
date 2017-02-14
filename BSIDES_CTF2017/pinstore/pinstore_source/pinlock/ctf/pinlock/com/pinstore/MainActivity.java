package pinlock.ctf.pinlock.com.pinstore;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.security.NoSuchAlgorithmException;

public class MainActivity extends AppCompatActivity {
    EditText pinEditText;

    /* renamed from: pinlock.ctf.pinlock.com.pinstore.MainActivity.1 */
    class C01741 implements OnClickListener {
        C01741() {
        }

        public void onClick(View view) {
            String enteredPin = MainActivity.this.pinEditText.getText().toString();
            String pinFromDB = null;
            String hashOfEnteredPin = null;
            try {
                pinFromDB = new DatabaseUtilities(MainActivity.this.getApplicationContext()).fetchPin();
            } catch (IOException e) {
                e.printStackTrace();
            }
            try {
                hashOfEnteredPin = CryptoUtilities.getHash(enteredPin);
            } catch (NoSuchAlgorithmException e2) {
                e2.printStackTrace();
            } catch (UnsupportedEncodingException e3) {
                e3.printStackTrace();
            }
            if (pinFromDB.equalsIgnoreCase(hashOfEnteredPin)) {
                Intent intent = new Intent(MainActivity.this, SecretDisplay.class);
                intent.putExtra("pin", enteredPin);
                MainActivity.this.startActivity(intent);
                return;
            }
            MainActivity.this.pinEditText.setText(BuildConfig.FLAVOR);
            Toast.makeText(MainActivity.this, "Incorrect Pin, try again", 1).show();
        }
    }

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView((int) C0175R.layout.activity_main);
        Button button = (Button) findViewById(C0175R.id.loginbutton);
        this.pinEditText = (EditText) findViewById(C0175R.id.pinedittext);
        button.setOnClickListener(new C01741());
    }
}
