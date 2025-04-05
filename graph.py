import plotly.graph_objs as go
import numpy as np

def pastel_gradient(n, base_color, alpha_start=0.5, alpha_end=0.9, darken_factor=0.2):
    alphas = np.linspace(alpha_start, alpha_end, n)  # Smooth gradient
    shades = []
    for i, alpha in enumerate(alphas):
        darkened_color = tuple(max(0, c - (i * darken_factor / n)) for c in base_color)
        shades.append('rgba({}, {}, {}, {})'.format(*(int(c * 255) for c in darkened_color), alpha))
    return shades

def generate_graphs():
    # Define spending categories and values
    categories = ["Housing", "Food", "Entertainment"]
    subcategories = [["Rent", "Utilities"], ["Groceries", "Dining Out"], ["Movies", "Games"]]
    vals = np.array([[50., 340], [40., 50.], [45., 70.]])  # Sub-category spending

    # Define total budget
    total_budget = 4000  # Example total monthly budget
    total_spent = vals.sum()  # Sum of all spending
    remaining = total_budget - total_spent  # Money left or over budget

    # Define number of categories
    num_main_categories = len(categories)
    num_subcategories = len(np.concatenate(subcategories))

    # Define base colors
    base_color_outer = (0.87, 0.73, 0.66)  # Pastel brown (#debaa9) - starts light
    base_color_inner = (0.74, 0.86, 0.81)  # Deep pastel green

    # Generate gradients
    outer_colors = pastel_gradient(num_main_categories, base_color_outer, alpha_start=0.5, alpha_end=0.85, darken_factor=0.3)  # Darker brown shades
    inner_colors = pastel_gradient(num_subcategories, base_color_inner, alpha_start=0.5, alpha_end=0.875,darken_factor=0.3)  # Green gradient

    # Create pie chart for spending breakdown
    fig_pie = go.Figure()
    fig_pie.add_trace(go.Pie(labels=categories, values=vals.sum(axis=1), hole=0.2, name="Main Categories", marker=dict(colors=outer_colors),
                             textinfo='label+percent', hoverinfo='label+value+percent', textposition='outside'))
    fig_pie.add_trace(go.Pie(labels=np.concatenate(subcategories), values=vals.flatten(), hole=0.6, name="Sub-categories", marker=dict(colors=inner_colors),
                             textinfo='label+percent', hoverinfo='label+value+percent', textposition='inside', insidetextorientation='horizontal'))

    fig_pie.update_layout(
        title_text="Spending Breakdown",
        font=dict(
            family="Noto Sans, sans-serif",  # Change to your preferred font
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
            family="Noto Sans, sans-serif",  # Change to your preferred font
            size=14,  # Change to your preferred font size
            color="#8b4900"  # Change to your preferred font color
        )
    )

    # Return HTML representation of the graphs
    pie_html = fig_pie.to_html(full_html=False)
    bar_html = fig_bar.to_html(full_html=False)

    return pie_html, bar_html
