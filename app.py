import base64
import os
import json
from cryptography.fernet import Fernet

# -------------------------------
# KEY MANAGEMENT
# -------------------------------
KEY_FILE = "secret.key"

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

key = load_or_create_key()
cipher = Fernet(key)

# -------------------------------
# PAN MASKING
# -------------------------------
def mask_pan(pan):
    return "**** **** **** " + pan[-4:]

# -------------------------------
# ENCRYPT PAN
# -------------------------------
def encrypt_pan(pan):
    pan_bytes = pan.encode()                 # string → bytes
    encrypted_bytes = cipher.encrypt(pan_bytes)  # AES encryption
    encoded = base64.b64encode(encrypted_bytes).decode()
    return encoded

# -------------------------------
# DECRYPT PAN
# -------------------------------
def decrypt_pan(encoded_pan):
    encrypted_bytes = base64.b64decode(encoded_pan.encode())
    decrypted_bytes = cipher.decrypt(encrypted_bytes)
    return decrypted_bytes.decode()

# -------------------------------
# TOKEN GENERATION
# -------------------------------
def generate_token():
    return "tok_" + base64.b32encode(os.urandom(5)).decode().replace("=", "").lower()

# -------------------------------
# MAIN FUNCTION
# -------------------------------
def main():
    print("===== Credit Card Encryption System =====")
    pan = input("Enter 16-digit PAN: ").strip()

    if not pan.isdigit() or len(pan) != 16:
        print("Invalid PAN format")
        return

    masked_pan = mask_pan(pan)
    encrypted_pan = encrypt_pan(pan)
    token = generate_token()

    print("\n--- OUTPUT ---")
    print("Masked PAN    :", masked_pan)
    print("Encrypted PAN :", encrypted_pan)
    print("Token         :", token)

    # Store securely
    data = {
        "token": token,
        "encrypted_pan": encrypted_pan
    }

    with open("storage.json", "w") as f:
        json.dump(data, f, indent=4)

    print("\nData stored securely (no raw PAN).")

    # Demonstrate decryption
    print("\n--- DECRYPTION TEST ---")
    decrypted_pan = decrypt_pan(encrypted_pan)
    print("Decrypted PAN :", decrypted_pan)

if __name__ == "__main__":
    main()
