import google.generativeai as genai

# Set API Key
API_KEY = "AIzaSyABMAcLWBV178zPub_j5LgJ0Jb253OPIKw"
genai.configure(api_key=API_KEY)

# Initialize the correct model
model = genai.GenerativeModel("gemini-2.0-flash") 

def get_budget_tips(income, rent, food, entertainment, savings):
    prompt = f"""
    You are a personal finance assistant. Based on the user's financial data, provide clear, actionable budgeting advice.

    **User's Financial Data:**
    - Income: ${income}
    - Rent: ${rent}
    - Food: ${food}
    - Entertainment: ${entertainment}
    - Savings: ${savings}

    Use best financial practices (e.g., 50/30/20 rule) to give tailored recommendations. Can you make the tailored recommendations more curt please
    """

    try:
        response = model.generate_content(prompt)
        return response.text if hasattr(response, "text") else "Unexpected response format."
    
    except Exception as e:
        return f"Error generating response: {e}"

# Example usage
if __name__ == "__main__":
    user_income = 4000
    user_rent = 1600
    user_food = 700
    user_entertainment = 450
    user_savings = 500

    budget_tips = get_budget_tips(user_income, user_rent, user_food, user_entertainment, user_savings)
    print(budget_tips)
