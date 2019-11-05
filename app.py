#!/usr/bin/env python3
from database import init_db
from flask import Flask, render_template
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

@app.route("/marks")
def marks():
    return render_template("pages/marks.html")

@app.route("/models")
def models():
    return render_template("pages/models.html")

app.add_url_rule(
    '/api',
    view_func=GraphQLView.as_view('version', schema=schema, graphiql=True)
)

if __name__ == '__main__':
    init_db()
    app.run()