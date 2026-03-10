# Import python packages
import streamlit as st
import snowflake.connector
from snowflake.snowpark import Session 
from snowflake.snowpark.functions import col

import requests
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fuit you want in your custom smoothie"""
)

name_on_order = st.text_input("Name on Smoothie")
st.write("Name on Smoothie will be:",name_on_order )


cnx = st.secrets["snowflake"]["account"]
session = Session.builder.configs(st.secrets["snowflake"]).create()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()


pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:',my_dataframe,max_selections=5
)
if ingredients_list:


    ingredients_string = ' '

    for fruit_choosen in ingredients_list:
      ingredients_string+=fruit_choosen

      search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      st.subheader(fruit_chosen + 'Nutrition Information')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}" + fruit_chosen)  
      sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""


    
    time_to_insert = st.button('Submit Orders')

    if time_to_insert:
        
        my_insert_stmt = f"""
        INSERT INTO ORDERS (NAME_ON_ORDER, INGREDIENTS)
        VALUES ('{name_on_order}', '{ingredients_string}')
        """
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

