import getpass
from utility.DataUtil import CreatePDF


user_name = ""
pasword = ""
login_token = ""

def ExecuteNew ():
    user_name = ""#input("Please provide the instagram user_name: ")
    password = ""#getpass.getpass("Password")
    login_token = CreatePDF(10)
    return

if __name__ == "__main__":
    ExecuteNew()