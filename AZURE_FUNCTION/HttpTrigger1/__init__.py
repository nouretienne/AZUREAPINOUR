import logging
import pandas as pd
import pickle
from surprise import SVD
import azure.functions as func


# charger le model

filename = 'model_azure.sav'
model_now = pickle.load(open(filename, 'rb'))

df = pd.read_csv('mini_df.csv')


# def recommend_items()
def recommend_items(uid,topn=5, algo=model_now):
    """
    prend en entrée le user _id et renvoie les tops recommendataion
    """

    iid_to_ignore=set(df[df["userID"]==int(uid)]["articles"])
    items2pred=pd.DataFrame(set(df.articles)-iid_to_ignore,columns=['articles'])
    items2pred['pred']=items2pred['articles'].apply(lambda x:model_now.predict(uid=int(uid), iid=x)[3])
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



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('user_id')
    # name = req.params.get('user_id')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('user_id')
            print('premier if ', name)

    if name:
        # liste = recommend_items(name)
        # convertir liste en str 
        # dans le HttpResponse mettre cette liste convertie en str

        return func.HttpResponse("Les articles a proposer pour l'utilisateur " + 
                                 str(name)  + " sont : " 
                                 + recommend_items(name,5, model_now))

       
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
