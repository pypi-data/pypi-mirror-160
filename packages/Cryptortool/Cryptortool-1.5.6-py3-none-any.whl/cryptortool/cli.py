try:
    from cryptortool.cryptortool import Cryptor
except ModuleNotFoundError:
    from cryptortool import Cryptor
def logo():
    import os
    os.system('cls||clear')
    print("""                                                                    
                                                                                                                                                                                                        
           ```````                                                    ```                         v.1.5.6      
        .ohdmNNNmdy/`                                                sddd`                              
      `sMMMMMNNNMMMMm:   ```  ````  ````     `````  ```   ````     `-MMMM.``     ```````      ````  ``` 
      sMMMMm:``.+MMMMN. -mmmh/dMMd -mmmmy   `dmmmo ommmoodNMMNh:  /mNMMMMmmy   :ydNMMMNdy:   `mmmd/dNMN 
      NMMMM/     +ssss. -MMMMMMMMm  oMMMM:  +MMMm` sMMMMMdhmMMMM+ :hNMMMMhhs `hMMMNysyNMMMh` `MMMMMMMMN 
     `MMMMM:            -MMMMN/..`   hMMMm `NMMM-  sMMMM/   dMMMN   yMMMM`   +MMMM:   :MMMM+ `MMMMN+..` 
      mMMMMs     sNNNN- -MMMMs       `mMMM+oMMMo   sMMMM.   hMMMM   yMMMM`   sMMMM.   .MMMMs `MMMMy     
      :MMMMMh+/+hMMMMd  -MMMMo        -NMMNNMMh    sMMMMh--/NMMMd   yMMMM:`  :MMMMs.`.sMMMM- `MMMMy     
       -hMMMMMMMMMMNs`  -MMMMo         /MMMMMN.    sMMMMMMMMMMMm.   +MMMMMMh  :mMMMMMMMMMd:  `MMMMy     
         `:osyyss+:`    `oooo:          dMMMM/     sMMMM:/syso:`     -osyys/    -+ssyss+-    `oooo:     
                                    /yydMMMN+      sMMMM-                                               
                                    omNNNds.       +dddd.                                               
                                     `````          ````                                                
    """)
def main():
    import getpass
    logo()
    cryptor = Cryptor()
    print("Menu: ")
    print("1 - Encrypt or Decrypt text\n2 - Encrypt or Decrypt file\n3 - Encrypt or Decrypt text in photo(PNG only)\n4 - Exit")
    FileOrText = input("[+] What do you want to do? ").lower()
    if FileOrText == "1":
        logo()
        print("Menu: ")
        print("1 - Encrypt text\n2 - Decrypt text\n3 - Exit")
        mode = input("[+] What do you want to do? ").lower()
        if mode == "3":
            import sys
            sys.exit()
        data = input("[+] Enter text: ")
        print("--------------------")
        password = getpass.getpass("[+] Enter password: ")
        if mode == "1":
            encrypted = cryptor.encrypt(data, password, "AES-256-CBC")
            if "[Error]" in encrypted:
                print(encrypted)
            else:
                print("Encrypted text: "+str(encrypted))
        elif mode == "2":
            decrypted = cryptor.decrypt(data, password, "AES-256-CBC")
            if "[Error]" in decrypted:
                print(decrypted)
            else:
                print("Decrypted text: "+str(decrypted))    
        else:
            print("[Error] Unknown mode")
    elif FileOrText == "2":
        logo()
        print("Menu: ")
        print("1 - Encrypt file\n2 - Decrypt file\n3 - Exit")
        mode = input("[+] What do you want to do? ").lower()
        if mode == "3":
            import sys
            sys.exit()
        dir = input("[+] Enter file: ")
        print("--------------------")
        password = getpass.getpass("[+] Enter password: ")

        if mode == "1":
            cryptor.EncryptFile(dir, password)
        elif mode == "2":
            cryptor.DecryptFile(dir, password)
        else:
            print("[Error] Unknown mode")
    elif FileOrText == "3":
        logo()
        print("Menu: ")
        print("1 - Hide text in image\n2 - Show hidden text\n3 - Exit")
        mode = input("[+] What do you want to do? ").lower()
        if mode == "1":
            input_image = input("[+] Enter input image name: ")
            output_image = input("[+] Enter output image name: ")
            data = input("[+] Enter text: ")
            print("--------------------")
            password = getpass.getpass("[+] Enter password: ")
            stegano = lsb.hide(input_image, cryptor.encrypt(data, password, "AES-256-CBC"))
            stegano.save(output_image)
            print(f"[SUCCESS] Successfully hidden text in image({output_image})")
        if mode == "2":
            image = input("[+] Enter image name: ")
            print("--------------------")
            password = input("[+] Enter password: ")
            clear_message = lsb.reveal(image)
            print(f"Hidden text: {cryptor.decrypt(clear_message, password, 'AES-256-CBC')}")
        elif mode == "3":
            import sys
            sys.exit()
    elif FileOrText == "4":
        import sys
        sys.exit()
    else:
        print("[Error] Unknown mode")

if __name__ == "__main__":
    main()