import sqlite3

conn = sqlite3.connect('banking.db')

cursor = conn.cursor()

# cursor.execute("""create table bank(
#                name varchar(32), 
#                mail varchar(32) unique,
#                contact Number unique,
#                acc_no Number primary key,
#                pin varchar(10),
#                balance Number );""")
class InvalidCredentials(Exception):
    ...

class InvalidPattern(Exception):
    ...

class InsufficientBalance(Exception):
    ...



old1_acc_no = 798132726500

def register(name,mail,contact): # option 1:

    db_acc_no = cursor.execute('''select max(acc_no) from bank;''').fetchall()
    conn.commit()
    

    if db_acc_no[0][0] == None:
        acc_no = old1_acc_no
    else:
        acc_no = db_acc_no[0][0]+1

    cursor.execute(f'insert into bank (name, mail, contact, acc_no, pin, balance) values ("{name}","{mail}",{contact},{acc_no},"{None}",{500});')
    conn.commit()
    print(f"Successfully your account has registered and your account no is {acc_no}")



def pin_generation(acc_no,contact): # option 2
    db_contact = cursor.execute(f'select contact from bank where acc_no = {acc_no};').fetchall()
    print(db_contact)
    if db_contact[0][0] == contact:
        pin = input("enter the strong 4 digits pin").strip()
        encrypt_pin = ''.join([ chr(ord(i)+16) for i in pin ])
        print(encrypt_pin)
        if len(pin) == 4:
            cursor.execute(f"update bank set pin = '{encrypt_pin}' where acc_no = {acc_no};")
            conn.commit()
            print('Successfully pin was generated')
        else:
            raise InvalidPattern("enter only 4 digits pin")
        
    else:
        raise InvalidCredentials("Eigther account number or contact details are wrong")



def withdrawal(acc_no,pin): # option 3
    db_pin = cursor.execute(f'select pin from bank where acc_no = {acc_no};').fetchall()
    db_pin = ''.join([chr(ord(i)-16) for i in db_pin[0][0]])
    if db_pin == pin:
        amt = int(input("enter the amount to be withdrawal: ").strip())
        db_bal = cursor.execute(f'select balance from bank where acc_no = {acc_no};').fetchall()
        if amt <= db_bal[0][0]:
            bal = db_bal[0][0] - amt  
            cursor.execute(f'update bank set balance = {bal} where acc_no = {acc_no};')
            conn.commit()
            print('withdrawal succeeded')
        else:
            raise InsufficientBalance("Insufficient funds in account")
    else:
        raise InvalidCredentials("Eigther account number or pin is wrong")



def deposite(acc_no,pin): # option 4
    db_pin = cursor.execute(f'select pin from bank where acc_no = {acc_no};').fetchall()
    db_pin = ''.join([chr(ord(i)-16) for i in db_pin[0][0]])
    print(db_pin)
    if db_pin == pin:
        amt = int(input("enter the amount to be deposite: ").strip())
        db_bal = cursor.execute(f'select balance from bank where acc_no = {acc_no};').fetchall()
        bal = db_bal[0][0] + amt  
        cursor.execute(f'update bank set balance = {bal} where acc_no = {acc_no};')
        conn.commit()
        print('deposite succeeded')

    else:
        raise InvalidCredentials("Eigther account number or pin is wrong")

# deposite(798132726501,'2450')
def account_transfer(acc_no,pin,other_acc,other_contact): #option 5
    db_pin = cursor.execute(f'select pin from bank where acc_no = {acc_no};').fetchall()
    db_pin = ''.join([chr(ord(i)-16) for i in db_pin[0][0]])
    print(db_pin)
    if db_pin == pin:
        db_contact = cursor.execute(f'select contact from bank where acc_no = {other_acc};').fetchall()
        print(db_contact)
        if db_contact[0][0] == other_contact:
            amt = int(input("enter the amount you want too transfer: ").strip())
            db_bal = cursor.execute(f"select balance from bank where acc_no = {acc_no};").fetchall()
            print(db_bal)
            db_other_bal = cursor.execute(f'select balance from bank where acc_no = {other_acc};').fetchall()
            if amt <= db_bal[0][0]:
                bal = db_bal[0][0] - amt
                other_bal = db_other_bal[0][0] + amt
                cursor.execute(f'update bank set balance = {bal} where acc_no = {acc_no};')
                cursor.execute(f'update bank set balance = {other_bal} where acc_no = {other_acc};')
                conn.commit()
            else:
                raise InsufficientBalance("Insufficient funds to ttransfer")
        else:
            raise InvalidCredentials("Eigther tranfered account number or contact details are wrong")
    else:
        raise InvalidCredentials("Eigther account number or contact details are wrong")
    

while True:
    opt = int(input(f"""Choose the required option:\n1: Register
3: pin generation\n3: Withdrawal\n4: Deposite\n5:Account Transfer: """).strip())
    if opt == 1:
        name = input("enter your valid name: ").strip()
        mail = input("enter your valid mail: ").strip()
        contact = int(input("enter your valid contact: ").strip())
        register(name,mail,contact)
    elif opt == 2:
        acc_no = int(input("enter your valid account number: ").strip())
        contact = int(input("enter your valid contact number: ").strip())
        pin_generation(acc_no,contact)
    elif opt == 3:
        acc_no = int(input("enter your valid account number: ").strip())
        pin = input("enter your valid pin: ").strip()
        withdrawal(acc_no,pin)
    elif opt == 4:
        acc_no = int(input("enter your valid account number: ").strip())
        pin = input("enter your valid pin: ").strip()
        deposite(acc_no,pin)
    elif opt == 5:
        acc_no = int(input("enter your valid account number: ").strip())
        pin = input("enter your valid pin: ").strip()
        other_acc_no = int(input("enter your valid reference account number: ").strip())
        other_contact = int(input("enter your valid reference contact number: ").strip())
        account_transfer(acc_no,pin,other_acc_no,other_contact)
    else :
        break


