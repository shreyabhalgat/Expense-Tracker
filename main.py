import streamlit as st
import pandas as pd
import plotly.express as px

# Create an empty dataframe to store expenses
expenses = pd.DataFrame(columns=["Date", "Category", "Amount"])

# Title and description
st.title("Expense Tracker")
st.write("Track your daily expenses with this simple app.")

# Input expense details
date = st.date_input("Date", pd.to_datetime("today"))
category = st.selectbox("Category", ["Food", "Transportation", "Shopping", "Utilities", "Other"])
amount = st.number_input("Amount (in your currency)", value=0.00, step=1.0)

if st.button("Add Expense"):
    expenses = expenses.append({"Date": date, "Category": category, "Amount": amount}, ignore_index=True)

# Display current expenses
st.header("Your Expenses:")
st.write(expenses)

# Total expenses
total_expenses = expenses["Amount"].sum()
st.subheader(f"Total Expenses: {total_expenses}")

# Expense by category
st.subheader("Expenses by Category:")
category_expenses = expenses.groupby("Category")["Amount"].sum()
fig = px.pie(category_expenses, values="Amount", names=category_expenses.index)
st.plotly_chart(fig)
