import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# CSV file path
FILE_PATH = "expenses.csv"

# Load or create the data
if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# Add a new expense
def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]],
                                columns=df.columns)
    updated_df = pd.concat([df, new_expense], ignore_index=True)
    updated_df.to_csv(FILE_PATH, index=False)
    st.success("Expense added!")

# Pie + Line chart
def show_charts(data):
    if not data.empty:
        st.subheader("📈 Monthly Expense Trend")
        data["Date"] = pd.to_datetime(data["Date"])
        monthly = data.groupby(data["Date"].dt.to_period("M"))["Amount"].sum()
        monthly.index = monthly.index.astype(str)
        st.line_chart(monthly)

        st.subheader("📊 Category-wise Expense Distribution")
        category_data = data.groupby("Category")["Amount"].sum()
        fig, ax = plt.subplots()
        ax.pie(category_data, labels=category_data.index, autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("No expenses found.")

# Streamlit UI
st.title("💸 Streamlit Expense Tracker")

menu = ["Add Expense", "View Expenses", "Visualize Expenses"]
choice = st.sidebar.selectbox("Select Option", menu)

if choice == "Add Expense":
    st.subheader("➕ Add New Expense")
    with st.form("expense_form"):
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Travel", "Rent", "Grocery", "Miscellaneous"])
        amount = st.number_input("Amount", min_value=0.0)
        description = st.text_input("Description (optional)")
        submitted = st.form_submit_button("Add")
        if submitted:
            add_expense(date, category, amount, description)

elif choice == "View Expenses":
    st.subheader("📋 All Expenses")
    st.dataframe(df)

elif choice == "Visualize Expenses":
    show_charts(df)
