import streamlit as st
import streamlit.components.v1 as com
from PIL import Image

image = Image.open('images/aboutimg.png')

def about():
    mystyle = '''
        <style>
            p {
                text-align: justify;
            }
        </style>
        '''
    st.markdown(mystyle, unsafe_allow_html=True)
    st.title("ABOUT US")
    st.write("---")
    st.write("##")
    st.header("OUR STORY")
    st.markdown("We are a group of students from BE IT and this is our Major Project for the year 2022-23.\n "
                "Since we are on the threshold of entering into our professional careers we realized that it is necessary to "
                "manage our finances efficiently from the beginning so that we have an insight of our net worth and spending patters.\n"
                "Developing this project not only improved our software skills but also gave us the opportunity to seek knowledge on "
                "finances, loan, budget and implement it in out lives.")
    st.write("---")
    st.header("MISSION")
    st.markdown("Personal finance plays a significant role in achieving financial freedom. The key to making successful financial decisions in today's "
                "fast-paced world is to manage money effectively by planning, organizing, directing, and controlling funds. "
                "Without good planning, we would be trapped, unsure of how to pay off debts and credit, as well as adequately pay "
                "our payments. Planning for retirement, college savings, and other personal assets may be involved while dealing with "
                "individuals in the field of finance management. The best way to accomplish your life goals is through managing your own finances. "
                "It is never too late to begin financial planning. At its most basic level, personal financial management comprises gaining a full "
                "understanding of your financial situation to maximize your assets in both present-day activities and long-term planning. "
                "This interface will be beneficial for all ordinary people. It will help you allocate your income to a budget that is within your means.")
    st.write("---")
    st.header("OUR TEAM")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Pooja Naik")
        st.markdown(
            "Instagram[![Instagram](https://img.icons8.com/material-outlined/48/000000/instagram.png)](https://www.instagram.com/poojanaik08)")
        st.markdown(
            "LinkedIn [![LinkedIn](https://img.icons8.com/material-outlined/48/000000/linkedin.png)](https://in.linkedin.com/in/pooja-naik-501a28131)")
        st.markdown(
            "GitHub [![GitHub](https://img.icons8.com/material-outlined/48/000000/github.png)](https://github.com/poojanaik08)")


    with col2:
        st.subheader("Tanvi Kurhade")
        st.markdown(
            "Instagram[![Instagram](https://img.icons8.com/material-outlined/48/000000/instagram.png)](https://www.instagram.com/tanvikurhade_)")
        st.markdown(
            "LinkedIn [![LinkedIn](https://img.icons8.com/material-outlined/48/000000/linkedin.png)](https://in.linkedin.com/in/tanvi-kurhade-693951241?trk=public_profile_samename-profile)")
        st.markdown(
            "GitHub [![GitHub](https://img.icons8.com/material-outlined/48/000000/github.png)](https://github.com/tanvikurhade)")


    with col3:
        st.subheader("Atharv Khanvilkar")
        st.markdown(
            "Instagram[![Instagram](https://img.icons8.com/material-outlined/48/000000/instagram.png)](https://www.instagram.com/adk_1410)")
        st.markdown(
            "LinkedIn [![LinkedIn](https://img.icons8.com/material-outlined/48/000000/linkedin.png)](https://in.linkedin.com/in/tanvi-kurhade-693951241?trk=public_profile_samename-profile)")
        st.markdown(
            "GitHub [![GitHub](https://img.icons8.com/material-outlined/48/000000/github.png)](https://github.com/tanvikurhade)")


    st.write("---")


    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("style/style.css")

    with st.container():

        st.subheader("Get In Touch With Us!")
        st.write("##")
        contact_col, contact_img_col = st.columns([1.5,0.9], gap="large")
        with contact_col:
            contact_form= """
            <form action="https://formsubmit.co/adk14102001@gmail.com" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your Name" required>
                <input type="email" name="email" placeholder="Your Email" required>
                <textarea name="message" placeholder="Your message here" required></textarea>
                <button type="submit">Send</button>
            </form>
            """
            st.markdown(contact_form, unsafe_allow_html=True)
        
        with contact_img_col:
            st.image(image=image, width=500)