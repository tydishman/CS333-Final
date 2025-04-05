import google.generativeai as genai

# Set API Key
API_KEY = "AIzaSyABMAcLWBV178zPub_j5LgJ0Jb253OPIKw"
genai.configure(api_key=API_KEY)

# Initialize the correct model
model = genai.GenerativeModel("gemini-2.0-flash")

# Define the user's budget
total_budget = 4000  # Example budget (could be input by the user)

# Recurring payments (amount, frequency)
recurring_payments = [
    {"name": "Subscription A", "amount": 1000, "frequency": "monthly"},  # Example monthly subscription
    {"name": "Loan Payment", "amount": 2500, "frequency": "monthly"}  # Example monthly loan payment
]

# Function to get Gemini AI's buying advice with remaining budget
def get_buying_advice(item, remaining_budget):
    prompt = (f"Should I buy {item} now or wait for a better deal? "
              f"Consider discounts, seasonality, and demand trends, and other things you might think are helpful. "
              f"I have ${remaining_budget:.2f} left in my budget. "
              f"If I don't have enough budget for this item, dont tell me about the other factors and advise me to not buy it. "
              f"Make it concise and short.")
    response = model.generate_content(prompt)
    return response.text

# Wishlist and price input loop
wishlist = []
prices = {}

# User input for wishlist and prices
print("Welcome to your Wishlist Tracker! (Type 'done' when finished)")
while True:
    item = input("Enter an item for your wishlist: ")
    if item.lower() == "done":  
        break
    price = float(input(f"Enter the price of {item}: $"))
    wishlist.append(item)
    prices[item] = price

# Function to calculate if the user has enough budget considering recurring payments
def calculate_remaining_budget(initial_budget, recurring_payments):
    remaining_budget = initial_budget
    for payment in recurring_payments:
        remaining_budget -= payment["amount"]  # Subtract the recurring payment
    return remaining_budget

# Show buying advice based on budget and Gemini's recommendation
print("\n🔹 Buying Recommendations 🔹")
remaining_budget = calculate_remaining_budget(total_budget, recurring_payments)

for item in wishlist:
    item_price = prices[item]
    advice = get_buying_advice(item, remaining_budget)

    print(f"🛒 {item}: {advice}")
    
    if item_price <= remaining_budget:
        print(f"✅ You have enough budget for {item}. You can buy it now!")
        remaining_budget -= item_price
    else:
        print(f"❌ You don't have enough budget for {item}. You need an additional ${item_price - remaining_budget:.2f}.")
        remaining_budget -= item_price  # Allow the budget to go negative

# Display the remaining budget after considering the recurring payments and item purchases
print(f"\nRemaining budget: ${remaining_budget:.2f}")
