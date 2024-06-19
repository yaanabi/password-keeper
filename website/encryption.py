import os 
import base64
from cryptography.fernet import Fernet
from dotenv import load_dotenv, find_dotenv
import ast
load_dotenv(find_dotenv())

class Encryption:
    __f = Fernet(ast.literal_eval(os.environ['ENCRYPTION_KEY']))

    def encrypt_data(self, data):
        try:
            data = str(data)
            encrypted_data = self.__f.encrypt(data.encode('ascii'))
            encrypted_data = base64.urlsafe_b64encode(encrypted_data).decode("ascii")
            return encrypted_data
        except Exception as ex:
            print("Error(encrypt): ", ex)
    def decrypt_data(self, data):
        try:
            data = base64.urlsafe_b64decode(data)
            decrypted_data = self.__f.decrypt(data).decode('ascii')
            return decrypted_data
        except Exception as ex:
            print('Error(decrypt): ', ex)
    

e = Encryption()
print(e.decrypt_data(b'Z0FBQUFBQm1iMS1MSEd1VWhsUzVXSEo0UmlWRVhobHNXOVhKWmRKalFWckg2NzhuUnBSa0dUdm1TSnFDRkdRZmpxakF1TzVvSG9Vc2hWWlJEOGhudkJXN2l5eXRlWndWeFE9PQ=='))
