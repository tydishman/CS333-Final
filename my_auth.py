import db
from werkzeug.security import generate_password_hash, check_password_hash

DEFAULT_CATEGORIES = ["rent", "groceries", "spending", "paycheck", "savings"]

# Called by form
def create_user(username:str, email:str, raw_password:str):
    password_hash = generate_password_hash(raw_password)
    try:
        db.create_user(username, email, password_hash)
        user_id = db.get_user(username)['id']
        init_default_categories(user_id, DEFAULT_CATEGORIES)
        # Successfully added a new user
        success = True
    except:
        # Failed to add new user. Display this to caller
        success = False
    return success

def init_default_categories(user_id, categories_to_add):
    for category in categories_to_add:
        db.create_category(user_id, category)

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
    if(user_flag):
        user = db.get_user(identifier)
    else:
        user = None
    return user
