import plotly.graph_objs as go
import numpy as np

def main():
    pass

def pastel_gradient(n, base_color, alpha_start=0.5, alpha_end=0.9, darken_factor=0.2):
    alphas = np.linspace(alpha_start, alpha_end, n)  # Smooth gradient
    shades = []
    for i, alpha in enumerate(alphas):
        darkened_color = tuple(max(0, c - (i * darken_factor / n)) for c in base_color)
        shades.append('rgba({}, {}, {}, {})'.format(*(int(c * 255) for c in darkened_color), alpha))
    return shades

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

            
        # Define total budget
    total_budget = 5000.00
    remaining = total_budget - total_spent  # Money left or over budget


    # Define base colors
    base_color_outer = (0.87, 0.73, 0.66)  # Pastel brown (#debaa9) - starts light
    base_color_inner = (0.74, 0.86, 0.81)  # Deep pastel green

    # Generate gradients
    outer_colors = pastel_gradient(num_main_categories, base_color_outer, alpha_start=0.5, alpha_end=0.85, darken_factor=0.3)  # Darker brown shades
    inner_colors = pastel_gradient(num_subcategories, base_color_inner, alpha_start=0.5, alpha_end=0.875,darken_factor=0.3)  # Green gradient
    
    main_category_values = []
    for category_id in category_dict.keys():
        local_expense = 0.0
        for transaction in category_dict[category_id]:
            if(bool(transaction['expense'])):
                local_expense += transaction['value']
            else:
                local_expense -= transaction['value']
        main_category_values.append(local_expense)

    subcategory_values = []
    for title in subcategories:
        subcategory_values.append(sum(float(transaction['value']) for transaction in transaction_list if transaction['title'] == title))
    # Create pie chart for spending breakdown

    print(list(category_dict.keys()))
    print(subcategories)
    print()
    print(main_category_values)
    print(subcategory_values)
    # exit()

    # May need to rework the alignment on the two graphs
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(labels=list(category_dict.keys()), values=main_category_values, hole=0.2, name="Main Categories", marker=dict(colors=outer_colors),
                             textinfo='label+percent', hoverinfo='label+value+percent', textposition='outside'))
    fig_pie.add_trace(go.Pie(labels=subcategories, values=subcategory_values, hole=0.6, name="Sub-categories", marker=dict(colors=inner_colors),
                             textinfo='label+percent', hoverinfo='label+value+percent', textposition='inside', insidetextorientation='horizontal'))

    fig_pie.update_layout(
        title_text="Spending Breakdown",
        font=dict(
            family="Noto Sans, serif",  # Change to your preferred font
            size=14,  # Change to your preferred font size
            color="#8b4900"  # Change to your preferred font color
        )
    )

    fig_pie.show()

    print(category_dict)
    print(total_spent) 



    print(num_main_categories)
    print(num_subcategories)

if __name__ == "__main__":
    event1 = {'category_id':1, 'expense':1, 'value':13, 'title':"subcategory1"}
    event2 = {'category_id':1, 'expense':0, 'value':3, 'title':"subcategory2"}
    event3 = {'category_id':2, 'expense':1, 'value':17, 'title':"subcategory3"}
    event4 = {'category_id':3, 'expense':1, 'value':3, 'title':"subcategory4"}


    mylist = [event1, event2, event3, event4]
    generate_graphs(mylist)