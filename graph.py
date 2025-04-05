import matplotlib.pyplot as plt
import numpy as np

# Define spending categories and values
categories = ["Housing", "Food", "Entertainment"]
subcategories = [["Rent", "Utilities"], ["Groceries", "Dining Out"], ["Movies", "Games"]]
vals = np.array([[50., 340], [40., 50.], [45., 70.]])  # Sub-category spending

# Define total budget
total_budget = 4000  # Example total monthly budget
total_spent = vals.sum()  # Sum of all spending
remaining = total_budget - total_spent  # Money left or over budget

# Function to create a gradient of pastel shades
def pastel_gradient(n, base_color, alpha_start=0.5, alpha_end=0.9, darken_factor=0.2):
    """
    Generate a gradient of pastel shades smoothly varying from light to dark.
    The darken_factor makes each color slightly darker in the sequence.
    """
    alphas = np.linspace(alpha_start, alpha_end, n)  # Smooth gradient
    shades = []
    
    for i, alpha in enumerate(alphas):
        # Gradually darken the base color
        darkened_color = tuple(max(0, c - (i * darken_factor / n)) for c in base_color)
        shades.append([(1 - alpha) + alpha * c for c in darkened_color])

    return shades

# Define number of categories
num_main_categories = 3  
num_subcategories = 6  

# Define base colors
base_color_outer = (0.87, 0.73, 0.66)  # Pastel brown (#debaa9) - starts light
base_color_inner = (0.74, 0.86, 0.81)  # Deep pastel green

# Generate gradients
outer_colors = pastel_gradient(num_main_categories, base_color_outer, alpha_start=0.5, alpha_end=0.85, darken_factor=0.3)  # Darker brown shades
inner_colors = pastel_gradient(num_subcategories, base_color_inner, alpha_start=0.6, alpha_end=0.95)  # Green gradient

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(14, 7))  # 1 row, 2 columns (Pie + Bar Chart)
size = 0.3  # Thickness of the rings

# --------- PLOT PIE CHART ---------
# Outer pie (Main categories)
outer_wedges, outer_texts, _ = axes[0].pie(vals.sum(axis=1), radius=1, labels=categories, 
                                           autopct='%1.1f%%', pctdistance=0.9,  
                                           labeldistance=1.1,  
                                           colors=outer_colors, wedgeprops=dict(width=size, edgecolor='w'))

# Inner pie (Sub-categories)
inner_wedges, inner_texts, _ = axes[0].pie(vals.flatten(), radius=1-size, labels=np.concatenate(subcategories), 
                                           autopct='%1.1f%%', pctdistance=0.85,  
                                           labeldistance=1.2,  
                                           colors=inner_colors, wedgeprops=dict(width=size, edgecolor='w'))

axes[0].set(aspect="equal", title="Spending Breakdown (Pastel Brown & Green Gradient)")

# --------- PLOT BAR CHART ---------
labels = ["Budget", "Spent", "Remaining"]
values = [total_budget, total_spent, remaining]

bars = axes[1].bar(labels, values, color=["#debaa9", "#f6f0e4", "#bddbcf"])  # Using pastel brown for bars

# Add labels on top of bars
for bar in bars:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2, yval + 50, f"${yval}", ha='center', fontsize=12)

axes[1].set_ylabel("Amount ($)")
axes[1].set_title("Budget vs. Actual Spending")

# Show both charts
plt.tight_layout()
plt.show()
