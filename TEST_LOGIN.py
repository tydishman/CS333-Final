import db
from werkzeug.security import generate_password_hash, check_password_hash

def main():
    user = db.get_user("user@email.com")
    transactions = db.get_transactions_of_user(user)

    user2 = db.get_user("user2")
    transactions2 = db.get_transactions_of_user(user2)

    print('-' * 50)
    [print(transaction['title']) for transaction in transactions]
    print('-' * 50)
    [print(transaction['title']) for transaction in transactions2]
    print('-' * 50)
    print('-' * 50)

    categories = db.get_categories_of_user(user)
    [print(category['name']) for category in categories]


    # print_schema()

# Called by form
def create_user(username:str, email:str, raw_password:str):
    password_hash = generate_password_hash(raw_password)
    try:
        db.create_user(username, email, password_hash)
        # Successfully added a new user
        success = True
    except:
        # Failed to add new user. Display this to caller
        success = False
    return success

# Returns 
def login_user(identifier:str, raw_password:str):    
    try:
        db_user = db.get_user(identifier)
    except:
        return False
    
    if not db_user:
        return False

    db_hashed_pass = db_user['password_hash']
    if check_password_hash(db_hashed_pass, raw_password):
        # Successful hash match, login
        return True
    return False

def login_user_from_form(identifier, password):
    user_flag = login_user(identifier, password)
    print(user_flag)
    if(user_flag):
        user = db.get_user(identifier)
    else:
        user = None
    return user

if __name__ == "__main__":
    main()
    flag = input("Create user? y/n")
    if flag.lower() == "y":
        username = input("Username")
        email = input("Email")
        password = input("Pass")

        print(create_user(username, email, password))

    identifier = input("ID")
    password = input("Password")

    user = login_user_from_form(identifier, password)
    if(user):
        print(user['id'])
    else:
        print("Failed login")