from firebase_functions import https_fn, options
from firebase_admin import initialize_app
from recommend_store import recommend_store

initialize_app()


@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=[
            r"https://cheers-connect-e3c35.web.app",
            r"http://localhost:3000",
            r"https://cheers-connect-e3c35--.*-.*.web.app",
        ],
        cors_methods=["get", "post"],
    )
)
def execute(req: https_fn.Request) -> https_fn.Response:
    if req.path == "/":
        return https_fn.Response("It works!", status=200)
    elif req.path == "/recommend-store":
        return recommend_store(req)
    else:
        return https_fn.Response("Path is wrong!", status=400)
