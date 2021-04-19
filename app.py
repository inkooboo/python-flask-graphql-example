from flask import Flask
from flask_graphql import GraphQLView

from graphql_schema import make_schema_connector
from database import make_database_meta


def create_app():
    ''' Initialize top level Flask application object'''
    app = Flask(__name__)
    app.debug = True

    DbMeta = make_database_meta(app)

    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=make_schema_connector(DbMeta),
        graphiql=True,
    ))

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
