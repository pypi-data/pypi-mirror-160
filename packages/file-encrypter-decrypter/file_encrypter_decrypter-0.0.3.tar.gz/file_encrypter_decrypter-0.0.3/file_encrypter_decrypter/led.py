# import required module
# here secret keys are used with help to key ring which is not visible to user
import os
import sys

import cryptography
from cryptography.fernet import Fernet
import keyring


def generate_key(filename):
    old_data = keyring.get_password("os", filename)
    # print(old_data)
    if old_data is not None:
        # keyring.delete_password('os', filename)
        print(
            "You have already Encrypted the file once multiple encryption's on the same file is not "
            "allowed\nYou may want to decrypt the file ..."
        )
        input("\nPress Any Key to Exit")
        sys.exit()
    else:
        key = Fernet.generate_key()

        converted_key = key.decode(
            "utf-8"
        )  # converting key to string to be able to use with keyring
        # print("Secret Key has been generated")
        keyring.set_password(
            "os", filename, converted_key
        )  # saving the key with keyring, so we can use this later also
        key_saved = keyring.get_password("os", filename)
        if key_saved is not None:
            return converted_key.encode("utf-8")


def File_Encrypter(filepath):
    """
    use this to encrypt file , provide file path as argument

    """

    key = generate_key(filepath)

    # print(key)

    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(filepath, "rb") as file:
        data = file.read()
        # print(data)

    # encrypting the file
    encrypted = fernet.encrypt(data)
    # print("File Data has been encrypted")

    # opening the file in write mode and
    # writing the encrypted data
    with open(filepath, "wb") as file:
        file.write(encrypted)
        print("The file has been Encrypted Successfully")


# end def


def File_Decrypter(filename):
    """
    use this to decrypt file , provide file path as argument

    """
    # reading the key
    try:
        key_saved = keyring.get_password("os", filename)

        if key_saved is not None:
            # using the key
            fernet = Fernet(key_saved)

            # opening the encrypted file
            with open(filename, "rb") as enc_file:
                encrypted = enc_file.read()
                print("Loading Encrypted file data")

            # decrypting the file
            decrypted = fernet.decrypt(encrypted)
            print("Decrypting the file")

            # opening the file in write mode and
            # writing the decrypted data
            with open(filename, "wb") as dec_file:
                dec_file.write(decrypted)
                print("File data has been successfully decrypted")
            keyring.delete_password("os", filename)
            print("All data related to encryption  purged")

        else:
            print(
                "Sorry We dont have the required data to decrypt this file\nThe file may have been Decrypted "
                "already"
            )
    except cryptography.fernet.InvalidToken:
        print("Oops the file provided is not encrypted using this module")


file_counter = 0


def Folder_Encrypter(folderpath):
    global file_counter
    for filename in os.listdir(folderpath):
        filee = os.path.join(folderpath, filename)
        if os.path.exists(filee):
            File_Encrypter(filee)
            file_counter += 1
    print(
        f"Total files in folder - {len(os.listdir(folderpath))}\nTotal Encrypted successfully - {file_counter} "
    )


def Folder_Decrypter(folderpath):
    global file_counter
    for filename in os.listdir(folderpath):
        filee = os.path.join(folderpath, filename)
        if os.path.exists(filee):
            File_Decrypter(filee)
            file_counter += 1
    print(
        f"Total files in folder - {len(os.listdir(folderpath))}\nTotal Decryption run - {file_counter} "
    )


# File_Encrypter("sample.pdf")
# File_Decrypter("sample.pdf")
