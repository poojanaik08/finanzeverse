import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_lottie import st_lottie
from PIL import Image

from f1 import f1

def login():
    image = Image.open("images/loginimg.png")
    with open('config.yaml') as file:
        config = yaml.load(file,Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    name, authentication_status, username = authenticator.login("Login", "main")
    if authentication_status:
        authenticator.logout('Logout', 'sidebar')
        st.sidebar.write(f'Welcome *{name}*')
        if username == 'admin':
            st.title("Admin Page")
            st.text("You now have admin rights")
        else:
            #sample()
            f1()
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
