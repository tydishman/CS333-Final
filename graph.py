import plotly.graph_objs as go
import numpy as np
from datetime import datetime
import db

def pastel_gradient(n, base_color, alpha_start=0.5, alpha_end=0.9, darken_factor=0.2):
    alphas = np.linspace(alpha_start, alpha_end, n)
    shades = []
    for i, alpha in enumerate(alphas):
        darkened_color = tuple(max(0, c - (i * darken_factor / n)) for c in base_color)
        shades.append('rgba({}, {}, {}, {})'.format(*(int(c * 255) for c in darkened_color), alpha))
    return shades

def generate_graphs(transaction_list, total_budget):
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    total_spent = 0.0
    category_dict = {}
    translation_dict = {}
    subcategories = []
    num_main_categories = 0
    num_subcategories = 0

    # Filter transactions by current month
    filtered_transactions = []
    for transaction in transaction_list:
        transaction_date = datetime.strptime(transaction['created_at'], "%Y-%m-%d")
        if transaction_date.year == current_year and transaction_date.month == current_month:
            filtered_transactions.append(transaction)

            category_id = str(transaction['category_id'])
            try:
                category_dict[category_id].append(transaction)
            except KeyError:
                category_dict[category_id] = [transaction]
                num_main_categories += 1

            if transaction['title'] not in subcategories:
                subcategories.append(transaction['title'])
                num_subcategories += 1

            if transaction['expense']:
                total_spent += float(transaction['amount'])

    for category_id in category_dict.keys():
        category_name = db.get_category_name_by_id(filtered_transactions[0]['user_id'], category_id)
        translation_dict[category_id] = category_name

    remaining = total_budget - total_spent

    # Colors
    base_color_outer = (0.87, 0.73, 0.66)
    base_color_inner = (0.74, 0.86, 0.81)
    outer_colors = pastel_gradient(num_main_categories, base_color_outer, alpha_start=0.5, alpha_end=0.85, darken_factor=0.3)
    inner_colors = pastel_gradient(num_subcategories, base_color_inner, alpha_start=0.5, alpha_end=0.875, darken_factor=0.3)

    # Main categories (filtered by current month)
    main_category_values = []
    for category_id in category_dict.keys():
        local_expense = 0.0
        for transaction in category_dict[category_id]:
            if transaction['expense']:
                local_expense += transaction['amount']
        main_category_values.append(local_expense)

    # Subcategories (filtered by current month)
    subcategory_values = []
    for title in subcategories:
        sub_total = sum(float(t['amount']) for t in filtered_transactions if t['title'] == title and t['expense'])
        subcategory_values.append(sub_total)

    # Pie chart
    in_labels = [translation_dict[cid].capitalize() for cid in translation_dict]

    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(
        labels=in_labels,
        values=main_category_values,
        hole=0.2,
        name="Main Categories",
        marker=dict(colors=outer_colors),
        textinfo='label+percent',
        hoverinfo='label+value+percent',
        textposition='outside'
    ))
    fig_pie.add_trace(go.Pie(
        labels=[x.capitalize() for x in subcategories],
        values=subcategory_values,
        hole=0.6,
        name="Sub-categories",
        marker=dict(colors=inner_colors),
        textinfo='label+percent',
        hoverinfo='label+value+percent',
        textposition='inside',
        insidetextorientation='horizontal'
    ))
    fig_pie.update_layout(
        title_text="Spending Breakdown",
        font=dict(
            family="Noto Sans, serif",
            size=14,
            color="#8b4900"
        )
    )

    # Bar chart
    labels = ["Budget", "Spent", "Remaining"]
    values = [total_budget, total_spent, remaining]
    fig_bar = go.Figure([go.Bar(
        x=labels,
        y=values,
        text=values,
        textposition='auto',
        marker=dict(color=["#debaa9", "#f6f0e4", "#bddbcf"])
    )])
    fig_bar.update_layout(
        title_text="Budget vs. Actual Spending",
        yaxis_title="Amount ($)",
        font=dict(
            family="Noto Sans, serif",
            size=14,
            color="#8b4900"
        ),
        plot_bgcolor="#fff9f5",
        paper_bgcolor="#ffffff"
    )

    # Return HTML
    pie_html = fig_pie.to_html(full_html=False)
    bar_html = fig_bar.to_html(full_html=False)

    return pie_html, bar_html