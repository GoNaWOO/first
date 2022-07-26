import streamlit as st
import sqlite3
import pandas as pd
import os.path



con = sqlite3.connect('db.db')
cur = con.cursor()

def login_user(id, pw):
    cur.execute(f"SELECT * FROM users WHERE id='{id}' and pwd = '{pw}'")
    return cur.fetchone()

menu = st.sidebar.selectbox('MENU', options=['로그인', '회원가입', '회원목록','이미지 크롭',])

if menu == '로그인':
    st.subheader('로그인')
    
    login_id = st.text_input('아이디',placeholder= '아이디를 입력하세요')
    login_pw = st.text_input('비밀번호', placeholder= '비밀번호를 입력하세요', type = 'password')
    login_btn = st.button('로그인')
    st.sidebar.subheader('로그인')

    if login_btn:
        user_info = login_user(login_id, login_pw)
        file_name = './img/'+user_info[0]+'.jpg'

        if os.path.exists(file_name):
            st.sidebar.image(file_name)
            st.write(user_info[4], '님 환영합니다.')
        else:
            st.write(user_info[4], '님 환영합니다.')





if menu == '회원가입':
    with st.form('my_form', clear_on_submit=True):
        st.info('다음 양식을 모두 입력 후 제출합니다.')
        uid = st.text_input('아이디', max_chars=12)
        uname = st.text_input('성명', max_chars=10)
        upwd = st.text_input('비밀번호', type='password')
        upwd_chk = st.text_input('비밀번호 확인', type='password')
        uage = st.text_input('나이')
        ugender = st.radio('성별', options=['남', '여'], horizontal=True)

        ubtn = st.form_submit_button('회원가입')
        if ubtn:
            if upwd != upwd_chk:
                st.error('비밀번호가 일치하지 않습니다.')
                st.stop()

            cur.execute(f"INSERT INTO users(id, pwd, name, age, gender) VALUES ("
                        f"'{uid}', '{upwd}', '{uname}','{uage}', '{ugender}')")
            con.commit()
            st.success('회원가입에 성공했습니다.')




if menu == '회원목록':
    st.subheader('회원목록')
    df = pd.read_sql('SELECT id, name,gender FROM users ', con)
    st.dataframe(df)
    st.sidebar.write('회원목록')

if menu == '이미지 크롭':
    import streamlit as st
    from streamlit_cropper import st_cropper
    from PIL import Image

    st.set_option('deprecation.showfileUploaderEncoding', False)

    # Upload an image and set some options for demo purposes
    st.header("Image Cropper")
    img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
    realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
    box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
    aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
    aspect_dict = {
        "1:1": (1, 1),
        "16:9": (16, 9),
        "4:3": (4, 3),
        "2:3": (2, 3),
        "Free": None
    }
    aspect_ratio = aspect_dict[aspect_choice]

    if img_file:
        img = Image.open(img_file)
        if not realtime_update:
            st.write("Double click to save crop")
        # Get a cropped image from the frontend
        cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                 aspect_ratio=aspect_ratio)

        # Manipulate cropped image at will
        st.write("Preview")
        _ = cropped_img.thumbnail((150, 150))
        st.image(cropped_img)










    






    



























