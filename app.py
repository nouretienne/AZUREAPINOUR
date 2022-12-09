import streamlit as st

import requests, json


st.text_input("Donnez l'identifiant de l'utilisateur", key="identifiant")

url = "https://azureapinour.azurewebsites.net/api/HttpTrigger1"
params = {'user_id':st.session_state.identifiant}
response = requests.get(url, params=params)

if st.session_state.identifiant:
    st.write("l'utilisateur d'identifiant", st.session_state.identifiant,"devrait aimer les articles", 
             response.text.split(':')[-1])
