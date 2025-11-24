from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from python_server.adapters.graphql.strawberry import graphql_app
from python_server.adapters.soap.soap_app import get_soap_app

app = FastAPI()

# Mount GraphQL under /graphql
app.mount("/graphql", graphql_app)
app.mount("/soap", WSGIMiddleware(get_soap_app()))
