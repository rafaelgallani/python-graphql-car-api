#!/usr/bin/env python3
from database import init_db
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
app.debug = True

default_query = '''
{
  allVersions {
    edges {
      node {
        id,
        name,
        model {
          id,
          name,
          mark {
            id,
            name,
            country
          }
        }
      }
    }
  }
}'''.strip()

app.add_url_rule(
    '/cars',
    view_func=GraphQLView.as_view('cars', schema=schema, graphiql=True)
)

if __name__ == '__main__':
    init_db()
    app.run()