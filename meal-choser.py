import ast
import requests
import streamlit as st
import pandas as pd
import numpy as np

# Get Sheet From Google API
r = requests.get(
    'https://sheets.googleapis.com/v4/spreadsheets/1aEK8c3xDDAetlMKmC11r37D82KRaq73bP7VGMgvETTU/values/sheet1?valueRenderOption=FORMATTED_VALUE&key=AIzaSyB1LRyMMyhUzs7ac8keUcBdBpEEHD-Zni8'
    ) 

# Convert bytes to dict and load as DataFrame
dictionnary = ast.literal_eval(r.content.decode('utf-8'))
df = pd.DataFrame(dictionnary['values'])
headers = df.iloc[0] 
new_df  = pd.DataFrame(df.values[1:], columns=headers) 

# Convert Columns Types
new_df['Distance'] = new_df['Distance'].astype(float)


bretzel_icon = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/pretzel_1f968.png"

# Set page title and favicon.
st.set_page_config(
    page_title="MealChooser", page_icon=bretzel_icon,
)


st.title('MealChooser')

# Filter Genre
genre = st.radio(
    "Meal Type",
    ('Warm', 'Cold'))
new_df = new_df[new_df['Warm/Cold'] == genre]



# Filter Here or Togo
where_options = np.unique(new_df['Here/ToGo'])
if len(where_options) > 1: 
    where = st.radio(
        "How",
        ('Here', 'ToGo'), index=1)
    new_df = new_df[new_df['Here/ToGo'] == where]



# Filter Distance
dist_min = float(new_df['Distance'].min())
dist_max = float(new_df['Distance'].max())
if dist_max != dist_min:
    values = st.slider(
        'Distance (km)',
        dist_min, dist_max, (dist_min, dist_max))
    new_df = new_df[new_df['Distance'] >= values[0]]
    new_df = new_df[new_df['Distance'] <= values[1]]

    

# Filter type of food
food_options = np.unique(new_df['Type'])
if len(food_options) > 1:
    options = st.multiselect(
        'Food Kind',
        food_options)

if st.button('Find Place'):
    if len(new_df) > 1:
        st.write(
            f" The Meal Chooser chosed for you : {new_df.sample(1)['Name'].iloc[0]} :yum:")
    elif len(new_df) == 1:
        st.write(f" You chose : {new_df['Name'].iloc[0]} :yum:")
    else:
        st.write("You are too difficult to satisfy :weary:")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
