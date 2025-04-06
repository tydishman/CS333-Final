import plotly.graph_objs as go
import numpy as np
import db

def pastel_gradient(n, base_color, alpha_start=0.5, alpha_end=0.9, darken_factor=0.2):
    alphas = np.linspace(alpha_start, alpha_end, n)  # Smooth gradient
    shades = []
    for i, alpha in enumerate(alphas):
        darkened_color = tuple(max(0, c - (i * darken_factor / n)) for c in base_color)
        shades.append('rgba({}, {}, {}, {})'.format(*(int(c * 255) for c in darkened_color), alpha))
    return shades

def generate_graphs(transaction_list, category_translations, total_budget):
    # Define spending categories and values
    # categories = ["Housing", "Food", "Entertainment"]
    # subcategories = [["Rent", "Utilities"], ["Groceries", "Dining Out"], ["Movies", "Games"]]
    # vals = np.array([[50., 340], [40., 50.], [45., 70.]])  # Sub-category spending

    total_spent = 0.0
    category_dict = {}
    translation_dict = {}   # key is category ID, value is category name
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

        value = float(transaction['amount'])
        if(bool(transaction['expense'])):
            total_spent += value
        else:
            total_spent -= value

    for category_id in category_dict.keys():
        category_name = db.get_category_name_by_id(transaction['user_id'], category_id)
        translation_dict[category_id] = category_name

    # Define total budget
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
                local_expense += transaction['amount']
            else:
                local_expense -= transaction['amount']
        main_category_values.append(local_expense)

    subcategory_values = []
    for title in subcategories:
        subcategory_values.append(sum(float(transaction['amount']) for transaction in transaction_list if transaction['title'] == title))
    # Create pie chart for spending breakdown

    in_labels = list(translation_dict.values())
    for i in range(len(in_labels)):
        in_labels[i] = in_labels[i].capitalize()

    # May need to rework the alignment on the two graphs
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(labels=in_labels, values=main_category_values, hole=0.2, name="Main Categories", marker=dict(colors=outer_colors),
                             textinfo='label+percent', hoverinfo='label+value+percent', textposition='outside'))
    fig_pie.add_trace(go.Pie(labels=[x.capitalize() for x in subcategories], values=subcategory_values, hole=0.6, name="Sub-categories", marker=dict(colors=inner_colors),
                             textinfo='label+percent', hoverinfo='label+value+percent', textposition='inside', insidetextorientation='horizontal'))

    fig_pie.update_layout(
        title_text="Spending Breakdown",
        font=dict(
            family="Noto Sans, serif",  # Change to your preferred font
            size=14,  # Change to your preferred font size
            color="#8b4900"  # Change to your preferred font color
        )
    )

    # Create bar chart for budget vs. actual spending
    labels = ["Budget", "Spent", "Remaining"]
    values = [total_budget, total_spent, remaining]

    fig_bar = go.Figure([go.Bar(x=labels, y=values, text=values, textposition='auto', marker=dict(color=["#debaa9", "#f6f0e4", "#bddbcf"]))])
    fig_bar.update_layout(
        title_text="Budget vs. Actual Spending",
        yaxis_title="Amount ($)",
        font=dict(
            family="Noto Sans, serif",
            size=14,
            color="#8b4900"
        ),
        plot_bgcolor="#fff9f5",   # Inside the graph area
        paper_bgcolor="#ffffff"   # Around the graph area
    )

    # Return HTML representation of the graphs
    pie_html = fig_pie.to_html(full_html=False)
    bar_html = fig_bar.to_html(full_html=False)

    # fig_pie.show()

    return pie_html, bar_html

if __name__ == "__main__":
    generate_graphs()