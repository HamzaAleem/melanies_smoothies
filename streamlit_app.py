# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Title
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write("Choose the fruit you want in your custom smoothie")

# Name input
name_on_order = st.text_input("Name on Smoothie")
st.write("Name on Smoothie will be:", name_on_order)

# ❌ Remove this debug line in production
# st.write(st.secrets)

# ✅ Create Snowpark session
session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# ✅ Fetch fruit options
fruit_df = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
fruit_list = [row['FRUIT_NAME'] for row in fruit_df.collect()]  # convert to Python list

# Multi-select for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

# Handle selection
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)

    # Submit button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS (NAME_ON_ORDER, INGREDIENTS)
        VALUES ('{name_on_order}', '{ingredients_string}')
        """
        session.sql(insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
