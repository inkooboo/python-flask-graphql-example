from user import make_user_connector
import graphene


def make_schema_connector(DbMeta):
    '''Define GraphQL schema'''

    _user, _update_user, _add_user, _remove_user = make_user_connector(DbMeta)

    class Queries(graphene.ObjectType):
        user = _user

    class Mutations(graphene.ObjectType):
        update_user = _update_user
        add_user = _add_user
        remove_user = _remove_user

    return graphene.Schema(query=Queries, mutation=Mutations)
