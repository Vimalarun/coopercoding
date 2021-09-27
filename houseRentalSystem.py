import stdiomask
import getpass
import random
import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",password="vimal",database="houseRental")
mycursor = mydb.cursor()

class UserDetails:
    
    def login(self):
        email = input("Enter the Email: ")
        password = stdiomask.getpass(prompt="Enter the password: ")
        query = "SELECT email,password,uid FROM userdetails"
        mycursor.execute(query)
        result = mycursor.fetchall()
        id=0
        for i in result:
            if i[0]==email and i[1]==password:
                print("login successfully")
                id = i[2]
        return id

    def register(self):
        username = input("Enter the username: ")
        email = input("Enter the email: ")
        query = "SELECT email FROM userdetails"
        mycursor.execute(query)
        result = mycursor.fetchall()
        if email in result:
            print("User already exists login to continue!!")
        else:
            while True:
                mobileno = input("Enter the mobileNo: ")
                if len(mobileno)==10:
                    break
                else:
                    print("Enter a valid mobile no\n")
            password = stdiomask.getpass(prompt='Enter the password: ')
            while True:
                confirmpassword = stdiomask.getpass(prompt='Enter the password again to confirms: ')
                if password==confirmpassword:
                    break
                print("Enter the password correctly")
            query = "INSERT INTO userdetails (uname,email,phoneno,password) values(%s,%s,%s,%s)"
            value = (username,email,mobileno,password)
            mycursor.execute(query,value)
            mydb.commit()

class Tenant:
    def displayHouseDetails(self,userid):
        mycursor.execute('select * from housedetails where status=%s',('approved',))
        res = mycursor.fetchall()
        print("House details")
        for i in res:
            print(f"House id={i[0]}")
            print(f"Location={i[1]}")
            print(f"City={i[2]}")
            print(f"Square feet={i[3]}")
            print(f"Type={i[4]}")
            print(f"Rent={i[5]}")
            print("------------")

        ch = input("would you like to request enter yes: ")
        if ch=="yes":
            houseid = int(input("Enter the house id displayed in the screen: "))
            mycursor.execute('insert into tenantrequest (uid,hid,status) values(%s,%s,%s)',(userid,houseid,'request made'))
            mydb.commit()
            print("Your request has been to sent to the owner!!!")



class Owner:
    def houseDetails(self,id):
        option = input("Would you like to post enter yes: ")
        if option == "yes":
            print("Enter the house details to post:)")
            mycursor.execute('update userdetails set isOwner=%s where uid=%s'%(True,id))
            mydb.commit()
            query = "SELECT COUNT(*) FROM housedetails"
            mycursor.execute(query)
            res = mycursor.fetchall()
            hid = res[0][0]
            hid+=1
            location = input("Enter the location: ")
            city = input("Enter the city: ")
            sq = int(input("Enter the square feet: "))
            type = input("Enter the type: ")
            rent = int(input("Enter the rent: "))
            advertisement = input("Would you like to advertise enter yes: ")
            if advertisement=="yes":
                advertisement=True
            else:
                advertisement=False
            #inserting into house details
            mycursor.execute('insert into housedetails (hid,location,city,sq,type,rent,uid,advertisement) values(%s,%s,%s,%s,%s,%s,%s,%s)'
            ,(hid,location,city,sq,type,rent,id,advertisement))
            mydb.commit()

            #inserting into approver request
            apid = random.randint(1,3)
            mycursor.execute('insert into approverrequest (apid,hid) values(%s,%s)',(apid,hid))
            mydb.commit()
        else:
            mycursor.execute('select hid from housedetails where uid=%s',(id))
            res = mycursor.fetchall()
            print(res)
            pass



print("RENTAL SYSTEM")
print("1.User\n2.Approver\n3.Admin")
option = int(input("Enter the option: "))
if option==1:
    print("1.Login\n2.Register")
    option = int(input("Enter the option: "))
    u = UserDetails()
    while True:
        if option==1:
            id = u.login()
            break
        elif option==2:
            u.register()
            break
        else:
            print("Valid option")
    print("Press 1 to continue as Tenant")
    print("Press 2 to continue as Owner")
    option = int(input("Enter the option: "))
    while True:
        if option==1:
            t = Tenant()
            t.displayHouseDetails(id)
            break
        elif option==2:
            o = Owner()
            o.houseDetails(id)
            break
        else:
            print("Enter the valid option")

elif option==2:
    username = input("Enter the username: ")
    password = stdiomask.getpass(prompt="Enter the password: ")
    mycursor.execute('select * from approverdetails')
    res = mycursor.fetchall()
    flag=0
    for i in res:
        if i[1]==username and i[2]==password:
            apid = i[0]
            break
    mycursor.execute('select * from approverrequest where apid=%s AND STATUS IS NULL'%(apid))
    res = mycursor.fetchall()
    for i in res:
        check = input("Enter approved to approve or declined to decline: ")
        mycursor.execute('update housedetails set status=%s where hid=%s',(check,i[2]))
        mydb.commit()
        mycursor.execute('update approverrequest set status=%s where requestid=%s',("completed",i[0]))
        mydb.commit()