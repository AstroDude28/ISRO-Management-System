import pandas as pd
import mysql.connector as msc
global count
cou = 0
def startup():
    global cou
    try:
        global hos,use,passss
        a = pd.read_csv("C:\\ProgramData\\ISRO_log.csv")
        hos = a.iloc[0, 1]
        use = a.iloc[1, 1]
        passss = a.iloc[2, 1]
        connection = msc.connect(host=hos, user=use, password=passss)
        cursor = connection.cursor()
        print("_________________________________________MySQL connected successfully_________________________________________")
    except:
        if cou == 0:
            print("_________________________________________Enter login credentials_________________________________________")
        else:
            print("_________________________________________Invalid login credentials_________________________________________")
        hos = input("Enter host: ")
        use = input("Enter user: ")
        passss = input("Enter password: ")
        log = pd.DataFrame(data=[hos, use, passss])
        log.to_csv("C:\\ProgramData\\ISRO_log.csv")
        cou += 1
        startup()

if __name__ == '__main__':
    startup()