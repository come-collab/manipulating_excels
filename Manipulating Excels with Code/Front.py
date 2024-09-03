import streamlit as st
st.title("Manipulating excels with code")
col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.text_input(label="Nom")
with col2:
    st.text_input(label = "Kill")
with col3:
    st.text_input(label= "Points")


