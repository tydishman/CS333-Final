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

# Function to create pastel colors
def pastelize(color, alpha=0.5):
    """Blends a color with white to create a pastel shade."""
    return [(1 - alpha) + alpha * c for c in color]

# Define colors
tab20c = plt.cm.tab20c.colors  # Get base colors
outer_colors = [pastelize(tab20c[i]) for i in [0, 4, 8]]  # Pastel for main categories
inner_colors = [pastelize(tab20c[i]) for i in [1, 2, 5, 6, 9, 10]]  # Pastel for sub-categories

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(14, 7))  # 1 row, 2 columns (Pie + Bar Chart)

# --------- PLOT PIE CHART ---------
size = 0.3  # Thickness of the rings

# Outer pie (Main categories)
outer_wedges, outer_texts, _ = axes[0].pie(vals.sum(axis=1), radius=1, labels=categories, 
                                           autopct='%1.1f%%', pctdistance=0.9,  # Adjust pctdistance
                                           labeldistance=1.1,  # Adjust label distance
                                           colors=outer_colors, wedgeprops=dict(width=size, edgecolor='w'))

# Inner pie (Sub-categories)
inner_wedges, inner_texts, _ = axes[0].pie(vals.flatten(), radius=1-size, labels=np.concatenate(subcategories), 
                                           autopct='%1.1f%%', pctdistance=0.85,  # Adjust pctdistance
                                           labeldistance=1.2,  # Adjust label distance
                                           colors=inner_colors, wedgeprops=dict(width=size, edgecolor='w'))

axes[0].set(aspect="equal", title="Spending Breakdown (Pastel Colors)")

# --------- PLOT BAR CHART ---------
labels = ["Budget", "Spent", "Remaining"]
values = [total_budget, total_spent, remaining]

bars = axes[1].bar(labels, values, color=["#6fa990", "#f6f0e4", "#bddbcf"])

# Add labels on top of bars
for bar in bars:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2, yval + 50, f"${yval}", ha='center', fontsize=12)

axes[1].set_ylabel("Amount ($)")
axes[1].set_title("Budget vs. Actual Spending")

# Show both charts
plt.tight_layout()
plt.show()
