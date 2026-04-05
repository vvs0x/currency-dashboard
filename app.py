import streamlit as st

st.set_page_config(page_title="Currency Dashboard", layout="wide")
st.title("Currency Dashboard")
st.write("Hello, world!")

data = [1,2,3,4,5,6,7,8,9]
st.bar_chart(data, x_label='anything', y_label='anything2')

st.button('hello')