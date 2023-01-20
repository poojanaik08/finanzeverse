import streamlit as st
from PIL import Image
import hydralit_components as hc

from login import login
from signup import signup
from about import about

image = Image.open("images/logo_f.png")
page_title = "Finanzeverse"
page_icon = image
st.set_page_config(page_title=page_title, page_icon=image,layout="wide", initial_sidebar_state="collapsed")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    position: absolute;
    left: 0px;
    top: 0px;
    background: linear-gradient(175deg, rgba(24,24,24,1) 0%, rgba(48,8,70,1) 97%);
    backdrop-filter: blur(5px);
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
        """
st.markdown(hide_st_style, unsafe_allow_html=True)


def main():
    menu_data = [
        {'label':"Finanzeverse"},
        {'label':"Login"},
        {'label':"Signup"},
        {'label':"About"},
    ]
    over_theme = {'txc_inactive': 'white','menu_background':'purple','txc_active':'white','option_active':'black'}

    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
    )
    if menu_id == "Finanzeverse":
        st.title("Finanzeverse - The Personal Finance Manager")
    if menu_id == "Login":
        login()
    if menu_id == "Signup":
        signup()
    if menu_id == "About":
        about()


if __name__ == "__main__":
    main()