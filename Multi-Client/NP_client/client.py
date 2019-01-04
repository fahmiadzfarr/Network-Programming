import socket
import sys
import hashlib
import pyAesCrypt
import re
import datetime
import time


def user_file():
    fullname = ""
    gender = ""

    fullname = input("Enter fullname:")
    fullname = fullname.upper()
    if re.search(r'\bBIN\b', fullname):
        name_split = fullname.split("BIN")  # currently for malay user only
    else:
        name_split = fullname.split("BINTI")
    print(f"First name: {name_split[0]}")
    print(f"Last name :{name_split[1]}")

    ic = int(input("Enter ic: "))
    ic = str(ic)
    male_num = ("1", "3", "5", "7", "9")
    if ic.endswith(male_num):
        gender = "Male"
    else:
        gender = "Female"
    print(gender)
    num = int(input("Enter number of person (RM 10 /person) : "))
    totprc = int(num * 10)
    totprc = str(totprc)
    print("RM "+ totprc)

    born_year = ic[0:2]
    born_month = ic[2:4]
    born_day = ic[4:6]

    now = datetime.datetime.now()
    x = now.strftime("%c")

    #print(f"year {born_year} , month {born_month}, day{born_day} ")

    filename = fullname + ".txt"

    month = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November",12:"December"}

    born_month = month.get(int(born_month)) # get key
    
    f = open(filename, 'w')
    f.write(f"First name: {name_split[0]}\n")
    f.write(f"Last name: {name_split[1]}\n")
    f.write(f"IC Number: {ic}\n")
    f.write(f"Gender: {gender}\n")
    f.write(f"Age: {now.year - int(born_year)-1900}\n")
    f.write(f"Time: {x}\n")
    f.write(f"Number of person: {num}\n")
    f.write(f"RM: {totprc}\n")
    #f.write(f"Born Year: {int(born_year) + 1900}\n")
    #f.write(f"Born Month: {born_month}\n")
    #f.write(f"Born Day: {born_day}\n")


def hashmd5(filename):  # hash md5
    hasher = hashlib.md5()
    with open(filename, 'rb') as afile:
        buf = afile.read()
    hasher.update(buf)
    print(f"Hash from local : {hasher.hexdigest()}")
    hash_from_server = s.recv(1024).decode()
    print(f"Hash from server: {hash_from_server}")
    if hash_from_server != hasher.hexdigest():
        print("Hash value not same, file may be edited...")
    else:
        print("Hash value same with server")


def decrypt_file(passwordUser2):
    bufferSize = 64 * 1024
    password = "wak123"
    if(passwordUser2 == "wakwakwak"):
        filename = input("Enter filename to be decrypt: ")
        filename_aes = filename.replace("txt.aes", "txt")
        pyAesCrypt.decryptFile(filename, filename_aes, password, bufferSize)
    else:
        print("Wrong password !")
        time.sleep(2)
        menu()


def encrypt_file(passwordUser):
    # encryption/decryption buffer size - 64K
    bufferSize = 64 * 1024
    password = "wak123"
    if(passwordUser == "wakwakwak"):
        filename = input("Enter filename to be encrypt: ")
        filename_aes = filename + ".aes"
        pyAesCrypt.encryptFile(filename, filename_aes, password, bufferSize)
    else:
        print("Wrong password !")
        time.sleep(2)
        menu()
    # encrypt

    


def download(file_download):
    f = open(file_download, 'w')
    data = s.recv(1024)
    f.write(data.decode())
    f.close()


def upload(filename):
    f = open(filename, "r")
    bf = f.read().encode()  # read file content
    s.send(bf)
    print("File uploaded to server...")


def menu():
    print("\n\n")
    print(20 * "-", 5 * "#", "-", 3 * "#", "-", 3 * "#", 20 * "-")
    print(22 * "-", "#", 2 * "-", "#", "-", "#", "#", "-", "#", 19 * "-")
    print(21 * "-", "#", 3 * "-", "#", "-", "#", "#", "-", "#", 19 * "-")
    print(20 * "-", 5 * "#", "-", 3 * "#", "-", 3 * "#", 20 * "-")
    print("\n")
    print("1. Book Entrance")
    print("2. Upload File")
    print("3. Download File")
    print("4. Hash File")
    print("5. Encrypt File")
    print("6. Decrypt File")
    print("7. Exit")
    print(67 * "-")
    choice = (input("Enter choice [1-7]:  "))

    while True:

        if(choice == "1"):
            user_file()
        elif(choice == "2"):
            s.send(choice.encode())
            filename = input("Enter filename to be upload: ")
            s.send(filename.encode())
            upload(filename)
        elif(choice == "3"):
            s.send(choice.encode())
            file_download = input("Enter filename to download:  ")
            s.send(file_download.encode())
            download(file_download)
        elif(choice == "4"):
            s.send(choice.encode())
            filename = input("Enter filename to hash with server: ")
            s.send(filename.encode())
            hashmd5(filename)
        elif(choice == "5"):
            passwordUser = input("Enter password to encrypt : ")
            encrypt_file(passwordUser)
             # filename = input("Enter filename to be encrypt: ")
             # encrypt_file(filename)
             # print("File encrypted...")
        elif(choice == "6"):
            passwordUser2 = input("Enter password to decrypt : ")
            decrypt_file(passwordUser2)
            #filename = input("Enter filename to be decrypt: ")
            #decrypt_file(filename)
            #print("File decrypted...")
        elif (choice == "7"):
            exit(0)
        else:
            print("Invalid input")
            choice = 0
            menu()
        choice = 0
        time.sleep(2)
        menu()


host = str(sys.argv[1])
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
    menu()

    # ask the client whether he wants to continue
    ans = input('\nDo you want to continue(y/n) :')
    if ans == 'y':
        continue
    else:
        break
# close the connection
s.close()
