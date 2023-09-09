from firebase_functions import https_fn
from firebase_admin import initialize_app
from google.cloud import firestore

initialize_app()


@https_fn.on_request()
def stations(req: https_fn.Request) -> https_fn.Response:
    db = firestore.Client(project="cheers-connect-db-sandbox")
    list_documents = db.collection("station").list_documents()
    dic_dict_list = [doc_ref.get().to_dict() for doc_ref in list_documents]
    return https_fn.Response(dic_dict_list.__str__())
