import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for expenses if not already set
if 'expenses' not in st.session_state:
    st.session_state['expenses'] = []

st.title('Expense Tracker')

# Input fields for new expense
description = st.text_input('Description')
amount = st.number_input('Amount', min_value=0.0, format='%.2f')
category = st.selectbox('Category', ['Food', 'Transport', 'Utilities', 'Entertainment', 'Other'])
note = st.text_area('Note')
date = st.date_input('Date', value=datetime.today())

# Function to add expense
if st.button('Add Expense'):
    if description and amount > 0:
        st.session_state['expenses'].append({
            'description': description,
            'amount': amount,
            'category': category,
            'note': note,
            'date': date
        })
        st.success('Expense added!')
    else:
        st.error('Please enter a description and amount greater than 0.')

# Convert expenses to DataFrame for easier manipulation
if st.session_state['expenses']:
    df_expenses = pd.DataFrame(st.session_state['expenses'])
else:
    df_expenses = pd.DataFrame(columns=['description', 'amount', 'category', 'note', 'date'])

# Filter expenses by date
filter_date = st.date_input('Filter by date', value=None, key='filter_date')
if filter_date:
    df_expenses = df_expenses[df_expenses['date'] == pd.to_datetime(filter_date)]

# Display expenses with edit and delete options
st.subheader('Expenses')
if not df_expenses.empty:
    for index, row in df_expenses.iterrows():
        with st.expander(f"{row['description']} - ${row['amount']:.2f} [{row['category']}]"):
            st.write(f"Note: {row['note']}")
            st.write(f"Date: {row['date']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button('Edit', key=f"edit_{index}"):
                    # Populate form with existing data for editing
                    description_edit = st.text_input('Description', value=row['description'], key=f'desc_{index}')
                    amount_edit = st.number_input('Amount', min_value=0.0, value=row['amount'], format='%.2f', key=f'amt_{index}')
                    category_edit = st.selectbox('Category', ['Food', 'Transport', 'Utilities', 'Entertainment', 'Other'], index=['Food', 'Transport', 'Utilities', 'Entertainment', 'Other'].index(row['category']), key=f'cat_{index}')
                    note_edit = st.text_area('Note', value=row['note'], key=f'note_{index}')
                    date_edit = st.date_input('Date', value=row['date'], key=f'date_{index}')
                    if st.button('Save', key=f'save_{index}'):
                        # Save the edited expense
                        st.session_state['expenses'][index] = {
                            'description': description_edit,
                            'amount': amount_edit,
                            'category': category_edit,
                            'note': note_edit,
                            'date': date_edit
                        }
                        st.success('Expense updated!')
            with col2:
                if st.button('Delete', key=f"del_{index}"):
                    # Delete the expense
                    st.session_state['expenses'].pop(index)
                    st.success('Expense deleted!')
else:
    st.write('No expenses added yet.')

# Calculate total expenses
total = df_expenses['amount'].sum()
st.write(f"Total Expenses: ${total:.2f}")