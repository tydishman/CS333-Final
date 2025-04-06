import plotly.graph_objs as go
import numpy as np
from datetime import datetime
import db

def pastel_gradient(n, base_color, alpha_start=0.5, alpha_end=0.9, darken_factor=0.2):
    """Generate pastel RGBA colors with alpha fading and slight darkening."""
    alphas = np.linspace(alpha_start, alpha_end, n)
    shades = []
    for i, alpha in enumerate(alphas):
        darkened = tuple(max(0, c - (i * darken_factor / n)) for c in base_color)
        rgba = 'rgba({}, {}, {}, {})'.format(*(int(c * 255) for c in darkened), alpha)
        shades.append(rgba)
    return shades

def generate_graphs(transaction_list, base_budget):
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    total_income = 0.0
    total_spent = 0.0
    category_dict = {}
    subcategories = []

    # Filter and categorize current-month transactions
    filtered = []
    for txn in transaction_list:
        txn_date = datetime.strptime(txn['created_at'], "%Y-%m-%d")
        if txn_date.year == current_year and txn_date.month == current_month:
            filtered.append(txn)

            category_id = str(txn['category_id'])
            amount = float(txn['amount'])

            if txn['expense']:
                category_dict.setdefault(category_id, []).append(txn)
                
                if txn['title'] not in subcategories:
                    subcategories.append(txn['title'])

                total_spent += amount
            else:
                total_income += amount  # still used for adjusting budget


    # Determine budget logic
    if total_income > base_budget:
        effective_budget = total_income
        extra_income_used = True
    else:
        effective_budget = base_budget
        extra_income_used = False

    remaining = effective_budget - total_spent

    # Get readable category names
    translation_dict = {}
    if filtered:
        user_id = filtered[0]['user_id']
        for cat_id in category_dict:
            translation_dict[cat_id] = db.get_category_name_by_id(user_id, cat_id)

    # Generate color gradients
    outer_colors = pastel_gradient(len(category_dict), base_color=(0.87, 0.73, 0.66), alpha_start=0.5, alpha_end=0.85, darken_factor=0.3)
    inner_colors = pastel_gradient(len(subcategories), base_color=(0.74, 0.86, 0.81), alpha_start=0.5, alpha_end=0.875, darken_factor=0.3)

    # Prepare pie values
    main_category_values = [
        sum(t['amount'] for t in txns if t['expense'])
        for txns in category_dict.values()
    ]
    in_labels = [translation_dict[cid].capitalize() for cid in category_dict]

    subcategory_values = [
        sum(t['amount'] for t in filtered if t['title'] == title and t['expense'])
        for title in subcategories
    ]

    # Pie chart
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
        labels=[title.capitalize() for title in subcategories],
        values=subcategory_values,
        hole=0.6,
        name="Sub-categories",
        marker=dict(colors=inner_colors),
        textinfo='label+percent',
        hoverinfo='label+value+percent',
        textposition='inside',
        insidetextorientation='horizontal'
    ))

    # Title context
    pie_title = "Spending Breakdown"

    fig_pie.update_layout(
        title_text=pie_title,
        font=dict(family="Noto Sans, serif", size=14, color="#8b4900")
    )

    # Bar chart
    bar_labels = ["Preset Budget", "Income", "Effective Budget", "Spent", "Remaining"]
    bar_values = [base_budget, total_income, effective_budget, total_spent, remaining]
    bar_colors = ["#debaa9", "#c8e3d4", "#b0d9cf", "#f6f0e4", "#bddbcf"]

    fig_bar = go.Figure([go.Bar(
        x=bar_labels,
        y=bar_values,
        text=[f"${v:,.2f}" for v in bar_values],
        textposition='auto',
        marker=dict(color=bar_colors)
    )])
    fig_bar.update_layout(
        title_text="Budget vs. Actual Spending",
        yaxis_title="Amount ($)",
        font=dict(family="Noto Sans, serif", size=14, color="#8b4900"),
        plot_bgcolor="#fff9f5",
        paper_bgcolor="#ffffff"
    )

    # Return HTML output
    return fig_pie.to_html(full_html=False), fig_bar.to_html(full_html=False)