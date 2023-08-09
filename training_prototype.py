import streamlit as st
import json
from streamlit_lottie import st_lottie
import os
from PIL import Image
import io
import ast
import uuid

import numpy as np
import plotly.express as px
import pandas as pd

#----Lottie----#
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st.set_page_config(page_title='Training Prototype', page_icon=None, layout="centered")

st.title('ยินดีต้อนรับเข้าสู่ระบบ :violet[**Exercise Designer**]')

st.divider()

#----Tagging Zone----#
st.subheader(':red[Tagging Zone]')

master = pd.read_excel('data/physics_master_structure.xlsx')
database = pd.read_excel('data/database.xlsx')

master_col = st.columns(2)
Subj_list = master['Subjects'].drop_duplicates().to_list()
selected_subject = master_col[0].selectbox(':orange[**Subject**]', Subj_list, key='Subject')

filtered_master = master[master['Subjects'] == selected_subject]

Zone_list = filtered_master['Zones'].drop_duplicates().to_list()
selected_zone = master_col[1].selectbox(':orange[**Zone**]', Zone_list, key='Zone')

filtered_master = filtered_master[filtered_master['Zones'] == selected_zone]

Topic_list = filtered_master['Topics'].drop_duplicates().to_list()
selected_topic = master_col[0].selectbox(':orange[**Topic**]', Topic_list, key='Topic')

filtered_master = filtered_master[filtered_master['Topics'] == selected_topic]

SubTopic_list = filtered_master['Subtopics'].drop_duplicates().to_list()
selected_subtopic = master_col[1].selectbox(':orange[**Subtopic**]', SubTopic_list, key='Subtopic')

filtered_master = filtered_master[filtered_master['Subtopics'] == selected_subtopic]

Lesson_list = filtered_master['Lessons'].drop_duplicates().to_list()
selected_lesson = master_col[0].selectbox(':orange[**Lesson**]', Lesson_list, key='Lesson')

filtered_master = filtered_master[filtered_master['Lessons'] == selected_lesson]

# Assuming you have a DataFrame called 'master'
# Assuming you have a DataFrame called 'filtered_master' after filtering

#st.write(f'The current row is: {filtered_master.index[0]}')
st.write('The aviable keywords are: {}'.format(master.at[filtered_master.index[0],'Keywords']))
new_keyword = st.text_input('Add a new keyword here . . . ',value='Hello',key='new_keyword')
add_keyword_btn = st.button('Add a new keyword', key='add_keyword_button')

if add_keyword_btn:
    st.write(st.session_state['new_keyword'])
    if master.at[filtered_master.index[0],'Keywords'] != 'temp':
        master.at[filtered_master.index[0],'Keywords'] += ',' + st.session_state['new_keyword']
        master.to_excel('data/physics_master_structure.xlsx', index=False)
    if master.at[filtered_master.index[0],'Keywords'] == 'temp':
        master.at[filtered_master.index[0],'Keywords'] = st.session_state['new_keyword']
        master.to_excel('data/physics_master_structure.xlsx', index=False)


keyword_pool = master.at[filtered_master.index[0],'Keywords'].split(',')
keyword = st.columns(5)
keyword[0].selectbox(':orange[**$1^{st} Keyword$**]',keyword_pool,key='kw1')
keyword[1].selectbox(':orange[**$2^{nd} Keyword$**]',keyword_pool,key='kw2')
keyword[2].selectbox(':orange[**$3^{rd} Keyword$**]',keyword_pool,key='kw3')
keyword[3].selectbox(':orange[**$4^{th} Keyword$**]',keyword_pool,key='kw4')
keyword[4].selectbox(':orange[**$5^{th} Keyword$**]',keyword_pool,key='kw5')

diff_col = st.columns([3,5])
diff_lvl = diff_col[0].number_input('Difficulty Score',min_value=0,max_value=10,step=1,key='diff_lvl')
if diff_lvl >= 0 and diff_lvl <= 2:
    diff_col[1].subheader('')
    diff_rank = diff_col[1].subheader('Difficulty Grade: :green[C]')
elif diff_lvl >= 3 and diff_lvl <= 5:
    diff_col[1].subheader('')
    diff_rank = diff_col[1].subheader('Difficulty Grade: :blue[B]')
elif diff_lvl >= 6 and diff_lvl <= 8:
    diff_col[1].subheader('')
    diff_rank = diff_col[1].subheader('Difficulty Grade: :orange[A]')
elif diff_lvl >= 9 and diff_lvl <= 10:
    diff_col[1].subheader('')
    diff_rank = diff_col[1].subheader('Difficulty Grade: :red[S]')

st.divider()

#----Design and Preview Zone----#
st.subheader(':red[Exercise Design Zone]')
design, preview = st.columns(2,gap='medium')

example_txt = '''Type here . . .
'''
question = st.sidebar.text_area(':balloon: :green[**พิมพ์โจทย์ที่นี่ (ในรูป Markdown)**] :balloon:',height=200,key='question')

design_choice, design_image = st.columns(2)

ch1 = st.sidebar.text_area('Choice 1','this is your first choice',key='ch1')
ch2 = st.sidebar.text_area('Choice 2','my answer is $\\int f(x)dx$',height=10,key='ch2')
ch3 = st.sidebar.text_area('Choice 3','I choose this answer',height=10,key='ch3')
ch4 = st.sidebar.text_area('Choice 4','choice 4',height=10,key='ch4')
ch5 = st.sidebar.text_area('Choice 5','choice 5',height=10,key='ch5')

ch_correct = st.sidebar.number_input('The Correct Answer Is:', min_value=1, max_value=5,key='answer')
ch_width = st.sidebar.number_input("Left Width", min_value=1, max_value=10, step=1,key='ch_width')
image_width = st.sidebar.number_input("Right Width", min_value=1, max_value=10, step=1,key='img_width')
buff_width = st.sidebar.number_input("Buffer Width", min_value=1, max_value=10, step=1,key='buffer_width')
have_image = st.sidebar.checkbox('Have Image', key='have_image')
if have_image:
    illus_upload = st.sidebar.file_uploader('Upload your image here !!')

choice = [ch1, ch2, ch3, ch4, ch5]

st.write(':balloon: :green[**Exercise Preview**] :balloon:')
question_preview = st.markdown(question)

preview_choice, preview_image, preview_buffer = st.columns([ch_width,image_width,buff_width])
if st.session_state['have_image'] == True:
    if illus_upload is not None:
        illus = Image.open(illus_upload)
        preview_image.image(illus,use_column_width=True)



ch_preview = []
for i in range(5):
    ch_preview.append(preview_choice.checkbox(f'{i+1} . {choice[i]}', key=f'ch_preview{i}'))

for i in range(5):
    if i+1 != int(ch_correct):
        if ch_preview[i] == True:
            preview_choice.write(':sob: :blue[**Noooooooo**] :sob:')
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
    elif i+1 == int(ch_correct) and ch_preview[i] == True:
        preview_choice.write(':balloon: :green[**CongratZ!!**] :balloon:')
        st.balloons()

st.divider()

#----Solution and Preview Zone----#
st.subheader(':red[Solution Design Zone]')   
soln_col = st.columns([1,5])
soln_type = soln_col[0].radio('Solution Type',['Markdown','Image'],key='Soln_type')
if soln_type == 'Markdown':
    soln_markdown = soln_col[1].text_area('Type your solution here','Test Ja . . .', key='soln_markdown')
    soln_col[1].markdown(soln_markdown)
if soln_type == 'Image':
    soln_upload = soln_col[1].file_uploader('Uplaod your Solution Here')
    soln_image = Image.open(soln_upload)
    soln_col[1].image(soln_image)

st.divider()

#----Submitting Processes----#
submit_btn = st.button("Submit Exercise")
if submit_btn:
    exid = str(uuid.uuid4())
    st.write(exid)
    ex_path = os.path.join('data','exercises',exid)
    os.makedirs(ex_path)
    with open(os.path.join(ex_path,'question'),'w', encoding='utf-8') as f:
        f.write(st.session_state['question'])
        st.write('Question saved succesfully. . .:white_check_mark:')
    with open(os.path.join(ex_path,'question'),'r', encoding='utf-8') as f:
        st.markdown(f.read())

    if  st.session_state['have_image'] == True:
        image_path = os.path.join(ex_path,'image.png')
        with open(image_path,'wb') as f:
            img_byte_array = io.BytesIO()
            illus.save(img_byte_array, format='PNG')
            f.write(img_byte_array.getvalue())
            st.write('Image saved succesfully. . .:white_check_mark:')
           

    if st.session_state['Soln_type'] == 'Markdown':
        with open(os.path.join(ex_path,'soln'),'w', encoding='utf-8') as f:
            f.write(st.session_state['soln_markdown'])
            st.write('Solution Markdown saved succesfully. . .:white_check_mark:')
        with open(os.path.join(ex_path,'soln'),'r', encoding='utf-8') as f:
            st.markdown(f.read())

    if st.session_state['Soln_type'] == 'Image':
        with open(os.path.join(ex_path,'soln.png'),'wb') as f:
            img_byte_array = io.BytesIO()
            soln_image.save(img_byte_array, format='PNG')
            f.write(img_byte_array.getvalue())
            st.write('Solution Image saved succesfully. . .:white_check_mark:')
            
      

    for i in range(5):
        with open(os.path.join(ex_path,f'choice_{i+1}'),'w', encoding='utf-8') as f:
            f.write(st.session_state[f'ch{i+1}'])
            if i == 4:
                st.write(f'Choices saved succesfully. . .:white_check_mark:')

    ch_preview_again = []
    for i in range(5):
        with open(os.path.join(ex_path,f'choice_{i+1}'),'r', encoding='utf-8') as f:
            ch_preview_again.append(st.checkbox(f'{i+1} . {f.read()}', key=f'ch_preview_again{i}'))

    st.write(':balloon: All Processes is Done :balloon:')
    st.balloons()

    new_row = {
        'uid': exid,
        'Subject': st.session_state.Subject,
        'Zone': st.session_state.Zone,
        'Topic': st.session_state.Topic,
        'Subtopic': st.session_state.Subtopic,
        'Lesson': st.session_state.Lesson,
        'kw1': st.session_state.kw1,
        'kw2': st.session_state.kw2,
        'kw3': st.session_state.kw3,
        'kw4': st.session_state.kw4,
        'kw5': st.session_state.kw5,
        'lw': st.session_state.ch_width,
        'rw': st.session_state.img_width,
        'bw': st.session_state.buffer_width,
        'ans': st.session_state.answer,
        'have_image': st.session_state['have_image'],
        'diff': st.session_state['diff_lvl'],
        'soln': st.session_state['Soln_type']
    }
    new_row_df = pd.DataFrame([new_row])
    database = pd.concat([database, new_row_df], ignore_index=True)
    database.to_excel('data/database.xlsx', index=False)     


st.divider()
  