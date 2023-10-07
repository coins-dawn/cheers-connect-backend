from firebase_functions import https_fn
from firebase_admin import initialize_app
from google.cloud import firestore

initialize_app()


@https_fn.on_request()
def stations(req: https_fn.Request) -> https_fn.Response:
    db = firestore.Client(project="cheers-connect-db-sandbox")
    doc_ref = db.collection("station").document("station_list")
    doc_dict = doc_ref.get().to_dict()
    return https_fn.Response(doc_dict["station_list"].__str__())
