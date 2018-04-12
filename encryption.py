from cryptography.fernet import Fernet
import csv

def put_in_file(organisation,username,password):
    with open('detail.csv','w',newline='') as csvfile:
        fieldnames=['username','password','organisation']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'username':username,'password':password,'organisation':organisation})
    



def encrypt(organisation,username,password,key):
     
    cipher_suite=Fernet(key)
    pk=organisation.encode('ASCII')
    encoded_organisation=cipher_suite.encrypt(pk)
    pk=username.encode('ASCII')
    encoded_username=cipher_suite.encrypt(pk)
    pk=password.encode('ASCII')
    encoded_password=cipher_suite.encrypt(pk)
    put_in_file(encoded_organisation.decode('ASCII'),encoded_username.decode('ASCII'),encoded_password.decode('ASCII'))

def decrypt(data,key):
    f=Fernet(key)
    pk=bytes(data,'utf-8')
    pk=f.decrypt(pk)
    return pk.decode('ASCII')



def get_data(key):
    organisation=input("Enter organisation:")
    username=input("Enter username:")
    password=input("Enter password:")
    encrypt(organisation,username,password,key)

def show_file(organisation,key):
    
   with open('detail.csv','r',newline='') as csvfile:
       reader=csv.DictReader(csvfile)
       for row in reader:
           
           if organisation == decrypt(row['organisation'],key): 
               print('Organisation:',decrypt(row['organisation'],key),'Username:',decrypt(row['username'],key),'Password:',decrypt(row['password'],key))
               return
       print('Not found')

def regain(key):
    organisation=input('Enter Organisation:')
    show_file(organisation,key)


print("1.Enter new details.\n2.Regain Previous.")
option=input("Enter Your Option:")
if option == "1":
    key=Fernet.generate_key()
    get_data(key)
    print("Its done")
    print("Your Key is :",key.decode('ASCII'),"  Don't Share it." )
else:
    key=input("Enter your key:")
    regain(key.encode('ASCII'))


