"""import os
from openai import OpenAI

# Initialize Grok (xAI)
client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),   # safer than hardcoding
    base_url="https://api.x.ai/v1"
)

def chatbot_response(user_input, insights, df):
    try:
        # Convert insights list → text
        context = "\n".join(insights)

        # Strong prompt (important for good answers)
        prompt = f"""
"""You are a professional retail business consultant.

Analyze the dataset insights below and answer the question.

DATA INSIGHTS:
{context}

USER QUESTION:
{user_input}

INSTRUCTIONS:
- Give clear insights
- Suggest practical actions
- Keep answer short and useful
- Use bullet points if needed"""
"""

        # API call
        response = client.chat.completions.create(
            model="grok-beta",   # try "grok-1" or "grok-beta" if needed
            messages=[
                {"role": "system", "content": "You are a smart retail AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        # VERY IMPORTANT: show real error
        print("❌ GROK API ERROR:", e)

        # fallback so app never crashes
        return fallback_response(user_input, insights, df)


# ---------- FALLBACK (OFFLINE INTELLIGENCE) ----------
def fallback_response(user_input, insights, df):
    user_input = user_input.lower()

    if "increase sales" in user_input or "grow sales" in user_input:
        return (
            "📈 To increase sales:\n"
            "- Promote top-selling products\n"
            "- Offer combo deals\n"
            "- Give discounts on low-selling items\n"
            "- Improve product visibility"
        )

    elif "top product" in user_input or "best product" in user_input:
        if "Product" in df.columns and "Quantity" in df.columns:
            top = df.groupby("Product")["Quantity"].sum().idxmax()
            return f"🏆 Top selling product is: {top}"

    elif "revenue" in user_input:
        if "Price" in df.columns and "Quantity" in df.columns:
            revenue = (df["Price"] * df["Quantity"]).sum()
            return f"💰 Total revenue is ₹{revenue}"

    elif "low" in user_input:
        if "Product" in df.columns and "Quantity" in df.columns:
            low = df.groupby("Product")["Quantity"].sum().idxmin()
            return f"⚠️ Low performing product: {low}"

    elif "summary" in user_input:
        return "\n".join(insights)

    return "🤖 Try asking about sales, revenue, top products, or improvements." """