from sqlalchemy import Column, Integer, String
from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene


def make_user_connector(DbMeta):
    '''Make graphene schema connectors to query and mutate user'''

    class UserDbModel(DbMeta):
        __tablename__ = 'user'
        id = Column(
            Integer,
            primary_key=True,
            autoincrement=True,
            doc="Integer user id")
        name = Column(String, doc="User name")

    class User(SQLAlchemyObjectType):
        class Meta:
            model = UserDbModel

    def resolve_user(parent, info, id=None):
        query = User.get_query(info)
        if id:
            query = query.filter(UserDbModel.id == id)
        return query.all()

    _user = graphene.List(
        User,
        description="Query existing users",
        resolver=resolve_user,
        id=graphene.Int(description=UserDbModel.id.doc))

    class UpdateUser(graphene.Mutation):
        class Arguments:
            id = graphene.Int(required=True, description=UserDbModel.id.doc)
            name = graphene.String(
                required=True, description=UserDbModel.name.doc)

        user = graphene.Field(lambda: User, description="Updated user")

        def mutate(parent, info, id, name):
            query = User.get_query(info).filter(UserDbModel.id == id)
            assert 1 == query.update({UserDbModel.name: name})
            DbMeta.session.commit()
            return UpdateUser(user=query.first())

    _update_user = UpdateUser.Field(description="Update existing user")

    class AddUser(graphene.Mutation):
        class Arguments:
            name = graphene.String(
                required=True, description=UserDbModel.name.doc)

        user = graphene.Field(lambda: User, description="New user added")

        def mutate(parent, info, name):
            new_user = UserDbModel(name=name)
            DbMeta.session.add(new_user)
            DbMeta.session.commit()
            return AddUser(user=new_user)

    _add_user = AddUser.Field(description="Add new user")

    class RemoveUser(graphene.Mutation):
        class Arguments:
            id = graphene.Int(required=True, description=UserDbModel.id.doc)

        ok = graphene.Boolean()

        def mutate(parent, info, id):
            User.get_query(info).filter(UserDbModel.id == id).delete()
            DbMeta.session.commit()
            return RemoveUser(ok=True)

    _remove_user = RemoveUser.Field(description="Remove user")

    return _user, _update_user, _add_user, _remove_user
