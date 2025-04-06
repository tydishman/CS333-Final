def main():
    pass

def generate_graphs(transaction_list):
    total_spent = 0.0
    category_dict = {}
    subcategories = []
    num_main_categories = 0
    num_subcategories = 0
    
    # Initialize category dictionary
    for transaction in transaction_list:
        category_id = str(transaction['category_id'])

        try:
            category_dict[category_id].append(transaction)
        except KeyError:
            category_dict[category_id] = [transaction]
            num_main_categories += 1

        if transaction['title'] not in subcategories:
            subcategories.append(transaction['title'])
            num_subcategories += 1

        value = float(transaction['value'])
        if(bool(transaction['expense'])):
            total_spent += value
        else:
            total_spent -= value


    print(category_dict)
    print(total_spent) 



    print(num_main_categories)
    print(num_subcategories)

if __name__ == "__main__":
    event1 = {'category_id':1, 'expense':1, 'value':13, 'title':"one"}
    event2 = {'category_id':1, 'expense':0, 'value':3, 'title':"one"}
    event3 = {'category_id':2, 'expense':1, 'value':17, 'title':"two"}
    event4 = {'category_id':3, 'expense':1, 'value':3, 'title':"three"}


    mylist = [event1, event2, event3, event4]
    generate_graphs(mylist)