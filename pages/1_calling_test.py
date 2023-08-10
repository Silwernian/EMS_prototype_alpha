import streamlit as st
import json
from streamlit_lottie import st_lottie
import os
from PIL import Image
import ast

import numpy as np
import plotly.express as px
import pandas as pd

#----Lottie----#
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st.set_page_config(page_title='Training Prototype', page_icon=None, layout="centered")

database = pd.read_excel('data/database.xlsx')

st.dataframe(database)

#----Exercises Count----#
def count_folders(path):
    folder_count = 0
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            folder_count += 1
    return folder_count
target_path = "data/exercises/"
num_folders = count_folders(target_path)
st.header(f"Current Number of Exercises is: {num_folders}")

#----UID Input----#
uid_in = st.text_input(':orange[**Enter Ex.UUID here:**]','6198773c-fe0b-4f5a-9a09-24d4062093d2', key='uuid')

df_filtered = database[database['uid'] == st.session_state.uuid]
st.dataframe(df_filtered)
ex_index = df_filtered.index[0]
exid = df_filtered.loc[ex_index,'uid']
ex_path = os.path.join('data','exercises',exid)

st.divider()

#----Solution Zone----#
solution = st.expander(':green[**Show Solution**]')
with solution:
    if df_filtered.loc[ex_index,'soln'] == 'Image':
        with open(os.path.join(ex_path,'soln.png'), 'rb') as f:
            st.image(f.read())
    if df_filtered.loc[ex_index,'soln'] == 'Markdown':
        with open(os.path.join(ex_path,'soln'), 'r', encoding='utf-8') as f:
            st.markdown(f.read())


st.divider()
#----Exercises Zone----#
st.header(':violet[This is your Exercises:]')
#----question
with open(os.path.join(ex_path,'question'), 'r', encoding='utf-8') as f:
    st.markdown(f.read())
#----Layout
ch_column, img_column, buff_column = st.columns([df_filtered.loc[ex_index,'lw'],df_filtered.loc[ex_index,'rw'],df_filtered.loc[ex_index,'bw']])
#----Choices
choice = []
for i in range(5):
    with open(os.path.join(ex_path,f'choice_{i+1}'), 'r', encoding='utf-8') as f:
        choice.append(ch_column.checkbox(f'{i+1} .'+f.read(), key=f'choice{i}'))
ch_correct = df_filtered.loc[ex_index,'ans']
#----answer button
for i in range(5):
    if i+1 != int(ch_correct):
        if choice[i] == True:
            ch_column.write(':sob: :blue[**Noooooooo**] :sob:')
            cow = load_lottie('lottie_cow.json')
            st_lottie(
                cow,
                speed=1,
                reverse=False,
                loop=False,
                quality='high',
                height=None,
                width=None,
                key=None
               )
    elif i+1 == int(ch_correct) and choice[i] == True:
        ch_column.write(':balloon: :green[**CongratZ!!**] :balloon:')
        st.balloons()
#----image
if df_filtered.loc[ex_index,'have_image'] == True:
    with open(os.path.join(ex_path,'image.png'), 'rb') as f:
        img_column.image(f.read())

st.divider()




