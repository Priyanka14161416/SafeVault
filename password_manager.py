import sqlite3
from cryptography.fernet import Fernet
import os
import base64

DB_NAME = "accounts.db"
KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()
    
def get_fernet():
    key = load_key()
    return Fernet(key)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_account(website, username, password, fernet=None):
    if fernet is None:
        fernet = get_fernet()
    encrypted_password = fernet.encrypt(password.encode())
    encoded_password = base64.urlsafe_b64encode(encrypted_password).decode() 
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO accounts (website, username, password) VALUES (?, ?, ?)",
              (website, username, encoded_password))
    conn.commit()
    conn.close()

def get_accounts(fernet=None):
    if fernet is None:
        fernet = get_fernet()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT website, username, password FROM accounts")
    rows = c.fetchall()
    conn.close()

    accounts = []
    for row in rows:
        website, username, encoded_password = row
        try:
            encrypted_password = base64.urlsafe_b64decode(encoded_password.encode())
            password = fernet.decrypt(encrypted_password).decode()
            accounts.append((website, username, password))
        except Exception as e:
            print(f"Decryption failed for account ({website}, {username}): {e}")
    return accounts
