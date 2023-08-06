try:
    import pyAesCrypt, os, sys
    import requests as r
    from stegano import lsb
except ModuleNotFoundError:
    print("\n[Error] Module pyAesCrypt or requests or Stegano not found")
    modules = input("Do you want install them right now (Y/N)? ").lower()
    if modules == "y" or modules == "yes":
        import os, sys
        os.system("pip install pyAesCrypt requests stegano||pip3 install pyAesCrypt requests stegano")
        print("[SUCCESS] Successfully installed pyAesCrypt and requests\nPlease, restart program")
        sys.exit()
    else:
        import sys
        sys.exit()

class Cryptor:
    def __init__(self):
        self.PyVersion = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.CryptorVersion = "1.5.0"
        self.headers = {'user-agent': 'Python/'+self.PyVersion+' | Cryptor/'+self.CryptorVersion}
    def encrypt(self, data, key, method):
        enc = r.post(f"https://api.vaar.pp.ua/crypt/", data={"data": data, "key": key, "method": method, "mode": "e"}, headers=self.headers)
        status_code = enc.status_code
        enc = enc.json()
        if status_code == 200:
            return enc["text"]
        else:
            return "[Error] "+str(enc["message"])

    def decrypt(self, data, key, method):
        enc = r.post(f"https://api.vaar.pp.ua/crypt/", data={"data": data, "key": key, "method": method, "mode": "d"}, headers=self.headers)
        status_code = enc.status_code
        enc = enc.json()
        if status_code == 200:
            return enc["text"]
        else:
            return "[Error] "+str(enc["message"])
    def EncryptFile(self, file, password):
        bufferSize = 512*1024
        pyAesCrypt.encryptFile(
            str(file),
            str(file)+".aes",
            password,
            bufferSize
        )
        print(f"[SUCCESS]: File {file} successfully encrypted")
        delete = str(input("Do you want to delete original file (Y/N)? "))
        if delete.lower() == "y" or delete.lower() == "yes":
            os.remove(file)
            print("[INFO]: Original file was deleted")

    def DecryptFile(self, file, password):
        bufferSize = 512*1024
        try:
            pyAesCrypt.decryptFile(
                str(file),
                str(os.path.splitext(file)[0]),
                password,
                bufferSize
            )
            print(f"[SUCCESS]: File {file} successfully decrypted")
            delete = str(input("Do you want to delete encrypted file (Y/N)? "))
            if delete.lower() == "y" or delete.lower() == "yes":
                os.remove(file)
                print("[INFO]: Encrypted file was deleted")
        except:
            print("[Error]: Wrong password or file is damaged!")