"""import pandas as pd

def generate_insights(df):
    insights = []

    if "Product" in df.columns and "Quantity" in df.columns:
        top_product = df.groupby("Product")["Quantity"].sum().idxmax()
        insights.append(f"Top selling product is {top_product}")

    if "Price" in df.columns and "Quantity" in df.columns:
        revenue = (df["Price"] * df["Quantity"]).sum()
        insights.append(f"Total revenue is ₹{revenue}")

    if "Quantity" in df.columns:
        avg_sales = df["Quantity"].mean()
        insights.append(f"Average sales per transaction: {avg_sales:.2f}")

    return insights"""