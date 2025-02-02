from fastapi import FastAPI
import uvicorn
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from strawberry.schema.config import StrawberryConfig
import operator
import strawberry
from queries.queries_config import *
from strawberry.fastapi import GraphQLRouter

from flask import Flask
from strawberry.flask.views import GraphQLView
from strawberry.flask.views import AsyncGraphQLView

# def default_resolver(root, field):  #strawberry não permite o retorno de dicionários por padrão para isso é necessário fazer essa config
#     try:
#         return operator.getitem(root, field)
#     except KeyError as e:
#         return getattr(root, field)

def default_resolver(root, field):
    # Verifica se o campo existe antes de acessar
    if field in root:
        return root[field]
    else:
        return None  # Ou trate de outra forma, caso o campo não exist


config = StrawberryConfig(
    default_resolver=default_resolver
)

schema = strawberry.Schema(query=Query, config=config)

#integração de teste com o flask
app = Flask(__name__)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False) 
