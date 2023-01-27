import streamlit as st
import plotly.express as px
import pandas as pd

def main():
    st.title("File Upload")
    st.subheader("Home")
    st.subheader("Dataset")
    data_file = st.file_uploader("Upload CSV", type=['csv'])

    if st.button("Process"):
        if data_file is not None:
            df = pd.read_csv(data_file, index_col=False, encoding= 'utf-8-sig')
            st.dataframe(df)

            expense_df = df.loc[df["Type"]=="Expenses"]
            st.dataframe(expense_df)

            # component_group = expense_df.groupby(by=["Component"]).sum()[["Value"]].sort_values(by="Value", ascending=True)
            component_group = expense_df.groupby(by=["Component"]).agg({"Value": "sum", "Year": "unique"}).sort_values(by="Value", ascending=True)
            st.write(component_group)

            #TODO: add filters to year    
            fig = px.bar(
                component_group,
                x = "Value",
                y = component_group.index,
                orientation = 'h',
                template="plotly_white",
                hover_name= "Value",
                hover_data= ["Value"],
            )
            st.plotly_chart(fig)




if __name__ == '__main__':
    main()