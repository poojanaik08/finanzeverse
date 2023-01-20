import streamlit as st

import pandas as pd

def main():
    st.title("File Upload Tutorial")
    st.subheader("Dataset")
    data_file = st.file_uploader("Upload CSV", type=['csv'])

    if st.button("Process"):
        if data_file is not None:
            df = pd.read_csv(data_file, encoding= 'unicode_escape')
            st.dataframe(df)


if __name__ == '__main__':
    main()
