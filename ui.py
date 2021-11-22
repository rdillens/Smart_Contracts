import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import shelve

shelf_path = './resources/shelf'

def get_user():
    if not Path(shelf_path).is_dir():
        st.write("Hi, I don't believe we've met before...")
        # filepath = Path('./shelf')
        Path(shelf_path).mkdir(parents=True, exist_ok=True)        
    user_box = st.empty()
    with shelve.open(shelf_path + '/shelf') as sh:
        if 'username' in sh:
            username = sh['username']
            user_box.header(f"Hello {username}")
        else:
            with user_box.container():
                with user_box.form("add_user_form", clear_on_submit=False):
                    username = st.text_input("Enter username")
                    user_submit = st.form_submit_button("Add User")
                    if user_submit:
                        sh['username'] = username
                        user_box.success(f"Hello {username}!")
    return username


if __name__ == "__main__":
    load_dotenv()
    username = get_user()
    # st.write(f"Hello {username}")
