import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
streamlit.dataframe(fruits_to_show)

# create the repeatable code block

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice")
try:
# fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:  
       # streamlit.write('The user entered ', fruit_choice)
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)



# import requests

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
#        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response.json())

# take the json version of the response and normalize it 
#        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it as table
#        streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

# don't run anything past here while we troubleshoot
# streamlit.stop()

# import snowflake.connector

#streamlit.header("The fruit load list contains:")

streamlit.header("View Our Fruit List - Add Your Favorites")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
# add a button to load fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

    
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("SELECT * from fruit_load_list") 
# my_data_row = my_cur.fetchone()
# my_data_rows = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
# streamlit.text("The fruit load list contains:")
# streamlit.header("The fruit load list contains:")

# streamlit.text(my_data_row)
# streamlit.dataframe(my_data_row)
# streamlit.dataframe(my_data_rows)

# allow the user to add a fruit to the list

def insert_row_snowflake(new_fruit):
        with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')") 
            return "Thanks for adding " + new_fruit

# add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        back_from_function = insert_row_snowflake(add_my_fruit)
        my_cnx.close()
        streamlit.text(back_from_function)

# streamlit.write('Thanks for adding ', add_my_fruit)
# ---
# my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')") 
#   my_cur.execute("insert into fruit_load_list values ('from streamlit')") 

