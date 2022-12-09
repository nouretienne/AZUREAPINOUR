# librairie requests pour integrer l'api dans le dashboard

# creer un dossier dashboard puis un fichier dashboard.py 

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from surprise import SVD

filename = 'model_azure.sav'
model_now = pickle.load(open(filename, 'rb'))
df = pd.read_csv('mini_df.csv')

def recommend_items(uid,topn=5, algo=model_now):
    """
    prend en entrée le user _id et renvoie les tops recommendataion
    """
    iid_to_ignore=set(df.loc[df.userID==uid].articles)
    items2pred=pd.DataFrame(set(df.articles)-iid_to_ignore,columns=['articles'])
    items2pred['pred']=items2pred['articles'].apply(lambda x:model_now.predict(uid=uid, iid=x)[3])
    if topn==0:
        recommendations_df=items2pred.loc[:,['articles','pred']].sort_values(by='pred', ascending=False)
    else:
        recommendations_df=items2pred.loc[:,['articles','pred']].sort_values(by='pred', ascending=False).head(topn)
    result = list(recommendations_df.index)
    resultat = ""
    for i in range(5): 
        if i != 4:
            resultat += str(result[i]) + ", "
        else:
            resultat += str(result[i]) 
                  
    return resultat


st.text_input("Donnez l'identifiant de l'utilisateur", key="identifiant")
if st.session_state.identifiant:
    st.write("l'utilisateur d'identifiant", st.session_state.identifiant,"devrait aimer les articles", 
             recommend_items(int(st.session_state.identifiant),5,model_now))