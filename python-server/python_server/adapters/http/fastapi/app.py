from fastapi import FastAPI

from python_server.adapters.graphql.strawberry import graphql_app

app = FastAPI()

# Mount GraphQL under /graphql
app.mount("/graphql", graphql_app)
