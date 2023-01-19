import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image

@st.cache
def get_image():
    image = Image.open("images/signupimg.png")
    return image

import yaml
from yaml.loader import SafeLoader
def signup():
    c1,c2 = st.columns(2)
    with c1:
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
        
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized'])

        try:
            if authenticator.register_user('Signup', preauthorization=False):
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)
        
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
    
    with c2:
        image = get_image()
        st.image(image=image, width=670)