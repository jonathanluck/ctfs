package pinlock.ctf.pinlock.com.pinstore;

import android.support.v4.media.TransportMediator;
import android.util.Base64;
import android.util.Log;
import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import javax.crypto.Cipher;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;

public class CryptoUtilities {
    private Cipher cipher;
    private SecretKeySpec key;
    private String pin;

    public CryptoUtilities(String version, String pin) throws Exception {
        this.pin = pin;
        this.key = getKey(version);
        this.cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
    }

    public SecretKeySpec getKey(String version) throws Exception {
        if (version.equalsIgnoreCase("v1")) {
            Log.d("Version", version);
            return new SecretKeySpec(Arrays.copyOf(MessageDigest.getInstance("SHA-1").digest("t0ps3kr3tk3y".getBytes("UTF-8")), 16), "AES");
        }
        Log.d("Version", version);
        byte[] salt = "SampleSalt".getBytes();
        return new SecretKeySpec(SecretKeyFactory.getInstance("PBKDF2WithHmacSHA1").generateSecret(new PBEKeySpec(this.pin.toCharArray(), salt, 1000, TransportMediator.FLAG_KEY_MEDIA_NEXT)).getEncoded(), "AES");
    }

    public String encrypt(String plaintext) throws Exception {
        byte[] plaintextBytes = plaintext.getBytes();
        this.cipher.init(1, this.key);
        byte[] ciphertext = this.cipher.doFinal(plaintextBytes);
        Log.d("Status", Base64.encodeToString(ciphertext, 2));
        return Base64.encodeToString(ciphertext, 2);
    }

    public String decrypt(String ciphertext) throws Exception {
        byte[] ciphertextBytes = Base64.decode(ciphertext.getBytes(), 2);
        Log.d("Status", ciphertextBytes.toString());
        this.cipher.init(2, this.key);
        return new String(this.cipher.doFinal(ciphertextBytes), "UTF-8");
    }

    public static String getHash(String input) throws NoSuchAlgorithmException, UnsupportedEncodingException {
        String output = BuildConfig.FLAVOR;
        byte[] input_bytes = input.getBytes();
        MessageDigest md = null;
        try {
            md = MessageDigest.getInstance("SHA-1");
        } catch (NoSuchAlgorithmException e) {
        }
        md.update(input_bytes, 0, input_bytes.length);
        return getHex(md.digest());
    }

    public static String getHex(byte[] input) {
        String output = BuildConfig.FLAVOR;
        for (int i = 0; i < input.length; i++) {
            output = output + String.format("%02x", new Object[]{Byte.valueOf(input[i])});
        }
        return output;
    }
}
