# Import necessary libraries
import streamlit as st
from snowflake.snowpark.functions import col

# Title of the app
st.title("Customize your Smoothie 🥤")
st.write("Choose the fruits you want in your custom smoothie...")

# Get user input for the smoothie order name
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be:", name_on_order)

# Connect to Snowflake securely using Streamlit secrets
cnx = st.connection("snowflake", type="snowpark")
session = cnx.session()

# Fetch available fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
fruit_names = [row["FRUIT_NAME"] for row in my_dataframe]  # Convert to a list of names

# Display the available fruit options in a multiselect dropdown
ingredient_list = st.multiselect("Choose up to 5 ingredients:", fruit_names, max_selections=5)

# Process the selected ingredients
if ingredient_list:
    ingredients_string = ', '.join(ingredient_list)  # Convert list to comma-separated string

    # Define a parameterized SQL query
    my_insert_stmt = """
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES (:1, :2)
    """

    # Create a button for order submission
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).bind([ingredients_string, name_on_order]).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
