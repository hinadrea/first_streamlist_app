import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('π₯£Omega 3 & Blueberry Oatmeal')
streamlit.text('π₯Kale, Spinach & Rocket Smoothie')
streamlit.text('π Hard-Boiled Free-Range Egg')
streamlit.text('π₯π Avocado Toast')

streamlit.header('ππ₯­ Build Your Own Fruit Smoothie π₯π')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# Take the json version of the response and normalise it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output screen as table
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_rows1 = my_cur.fetchall()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows2 = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows2)

# Allow an end user to add another fruit to the list
streamlit.write("What fruit would you like to add?")
add_my_fruit = streamlit.text_input('What fruit would you like add','')
streamlit.write('The user entered ', add_my_fruit)

# Don't run anything past here while we troubleshoot
streamlit.stop

# This will not work correctly, just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
