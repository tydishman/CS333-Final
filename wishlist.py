import google.generativeai as genai

# Set API Key
API_KEY = "AIzaSyABMAcLWBV178zPub_j5LgJ0Jb253OPIKw"
genai.configure(api_key=API_KEY)

# Initialize the correct model
model = genai.GenerativeModel("gemini-2.0-flash")

# Define the user's budget
total_budget = 4000  # Example budget (could be input by the user)

# Function to get Gemini AI's buying advice
def get_buying_advice(item):
    prompt = f"Should I buy {item} now or wait for a better deal? Consider discounts, seasonality, and demand trends. make it concise"
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

# Show buying advice based on budget and Gemini's recommendation
print("\n🔹 Buying Recommendations 🔹")
remaining_budget = total_budget

for item in wishlist:
    item_price = prices[item]
    advice = get_buying_advice(item)

    print(f"🛒 {item}: {advice}")
    
    if item_price <= remaining_budget:
        print(f"✅ You have enough budget for {item}. You can buy it now!")
        remaining_budget -= item_price
    else:
        print(f"❌ You don't have enough budget for {item}. You need an additional ${item_price - remaining_budget:.2f}.")
        remaining_budget -= item_price  # Allow the budget to go negative

print(f"\nRemaining budget: ${remaining_budget:.2f}")
