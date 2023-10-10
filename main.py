import streamlit as st
import pandas as pd
import plotly.express as px

# session_state will help persist data within the same session
if not 'Date' in st.session_state:
    st.session_state['Date'] = []
    
if not 'Category' in st.session_state:
    st.session_state['Category'] = []
    
if not 'Amount' in st.session_state:
    st.session_state['Amount'] = []

# Create an empty dataframe to store expenses
expenses = pd.DataFrame(columns=["Date", "Category", "Amount"])

# Title and description
st.title("Expense Tracker")
st.write("Track your daily expenses with this simple app.")

# Input expense details
date = st.date_input("Date", pd.to_datetime("today"))
category = st.selectbox("Category", ["Food", "Transportation", "Shopping", "Utilities", "Other"])
amount = st.number_input("Amount (in your currency)", value=0.00, step=1.0)

if amount < 0:
    st.error("Amount must be a positive number.")
else:
    if st.button("Add Expense"):
        # append session_state lists
        st.session_state['Date'].append(date)
        st.session_state['Category'].append(category)
        st.session_state['Amount'].append(amount)
        expenses = pd.DataFrame({"Date": st.session_state['Date'], "Category": st.session_state['Category'], "Amount": st.session_state['Amount']})

    # Display current expenses
    st.header("Your Expenses:")
    st.write(expenses)

    # Total expenses
    total_expenses = expenses["Amount"].sum()
    st.subheader(f"Total Expenses: {total_expenses}")

    # Add export option
    if st.button("Export Expenses"):
        expenses.to_csv("expenses.csv", index=False)
        st.success("Expenses exported successfully.")

    # Expense by category Pie
    st.subheader("Pie Expenses by Category:")
    category_expenses = expenses.groupby("Category")["Amount"].sum()
    fig = px.pie(category_expenses, values="Amount", names=category_expenses.index)
    st.plotly_chart(fig)

    # Expense by category Bar
    st.subheader("Bar Expenses by Category:")
    fig = px.bar(category_expenses)
    st.plotly_chart(fig)

    # Add a form to edit and delete expenses
    exp_to_edit = st.selectbox("Select Expense to Edit or Delete", expenses["Date"])
    if st.button("Edit Expense"):
        new_amount = st.number_input("New Amount", value=0.00, step=1.0)
        expenses.loc[expenses["Date"] == exp_to_edit, "Amount"] = new_amount
        st.success("Expense edited successfully.")
    if st.button("Delete Expense"):
        expenses = expenses[expenses["Date"] != exp_to_edit]
        st.success("Expense deleted successfully.")
