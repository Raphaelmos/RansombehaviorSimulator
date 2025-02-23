# Ransom Behavior Simulator Attempt using also a VirtualBox 
# Still workingon it to look like a real one and not a key encrypt decrypt with gen
# VirtualBox 
"""
Have Python and the libraries
Use the command.
"""

# Ransom Behavior Simulator with Enhanced Features

from cryptography.fernet import Fernet
import os
import logging
import argparse
import shutil
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_key(key_file):
    key = Fernet.generate_key()
    with open(key_file, "wb") as kf:
        kf.write(key)
    logging.info(f"Encryption key saved to {key_file}")

def load_key(key_file):
    with open(key_file, "rb") as kf:
        return kf.read()

def encrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)
        
        encrypted_file_path = f"{file_path}.encrypted"
        with open(encrypted_file_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
        
        logging.info(f"File encrypted: {file_path} -> {encrypted_file_path}")
    except Exception as e:
        logging.error(f"Failed to encrypt {file_path}: {e}")

def decrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        original_file_path = file_path.replace(".encrypted", "")
        with open(original_file_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)
        
        logging.info(f"File decrypted: {file_path} -> {original_file_path}")
    except Exception as e:
        logging.error(f"Failed to decrypt {file_path}: {e}")

def backup_file(file_path):
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    logging.info(f"Backup created: {backup_path}")

def simulate_encryption(files_dir, key_file, extensions):
    if not os.path.exists(key_file):
        generate_key(key_file)
    
    key = load_key(key_file)
    
    for filename in os.listdir(files_dir):
        file_path = os.path.join(files_dir, filename)
        if os.path.isfile(file_path) and not filename.endswith(".encrypted"):
            if any(filename.endswith(ext) for ext in extensions):
                backup_file(file_path)
                encrypt_file(file_path, key)

def simulate_decryption(files_dir, key_file):
    if not os.path.exists(key_file):
        logging.error("Encryption key not found.")
        return
    
    key = load_key(key_file)
    
    for filename in os.listdir(files_dir):
        file_path = os.path.join(files_dir, filename)
        if os.path.isfile(file_path) and filename.endswith(".encrypted"):
            decrypt_file(file_path, key)

def main():
    parser = argparse.ArgumentParser(description="Ransomware Behavior Simulator")
    parser.add_argument('-d', '--directory', type=str, default='test_files', help='Directory containing files to encrypt/decrypt')
    parser.add_argument('-k', '--keyfile', type=str, default='key.key', help='Encryption key file')
    parser.add_argument('-e', '--encrypt', action='store_true', help='Simulate file encryption')
    parser.add_argument('-de', '--decrypt', action='store_true', help='Simulate file decryption')
    parser.add_argument('-ext', '--extensions', type=str, default='txt,jpg,png', help='Comma-separated file extensions to encrypt (default: txt,jpg,png)')

    args = parser.parse_args()

    extensions = args.extensions.split(',')

    if args.encrypt:
        simulate_encryption(args.directory, args.keyfile, extensions)
    elif args.decrypt:
        simulate_decryption(args.directory, args.keyfile)
    else:
        logging.error("No operation specified. Use --encrypt or --decrypt.")

if __name__ == "__main__":
    main()
