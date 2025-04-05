import db

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
   
if __name__ == "__main__":
    main()