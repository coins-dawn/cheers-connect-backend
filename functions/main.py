from firebase_functions import https_fn
from firebase_admin import initialize_app
from google.cloud import firestore

initialize_app()


@https_fn.on_request()
def stations(req: https_fn.Request) -> https_fn.Response:
    db = firestore.Client(project="cheers-connect-db-sandbox")
    documents = db.collection("station").stream()
    dic_dict_list = [doc.to_dict() for doc in documents]
    return https_fn.Response(dic_dict_list.__str__())
