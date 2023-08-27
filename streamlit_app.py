import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parent new healthy diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avacado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)



# create a definition
def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized
    
    

# new section to display fruityvice api response   
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("please select a fruit to get information.")
    else:
        back_from_fuction = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_fuction)
      #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      #streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()



streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
            my_cur.execute("select * from fruit_load_list ")
            return my_cur.fetchall()

# Add button to load the fruit
if streamlit.button('Get fruit load list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows = get_fruit_load_list()
      streamlit.dataframe(my_data_rows)



def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into fruit load_list values ('from streamlit') ")
            return "Thanks for adding" + new_fruit

add_my_fruit = streamlit.text_input('what fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function=insert_row_snowflake(add_my_fruit)
      streamlit.text(back_from_function)
 
            

#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#import requests 
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json()) 
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# Take  json version and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# output screen as a table 
#streamlit.dataframe(fruityvice_normalized)

streamlit.stop()

#import snowflake.connector

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()

#streamlit.write('Thanks for adding', add_my_fruit)
#my_cur.execute("select * from fruit_load_list ")
#my_cur.execute("insert into fruit_load_list values('from streamlit') ")
#my_data_rows = my_cur.fetchall()
#streamlit.header("The fruit load list contains")
#streamlit.dataframe(my_data_rows)

