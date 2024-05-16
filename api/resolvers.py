from ariadne import QueryType, MutationType
from database import TODO, User

query = QueryType()
mutation = MutationType()


@query.field("hello")
def resolve_hello(_, info):
    """Returns a hello message with User-Agent's property."""
    request = info.context
    user_agent = request.headers.get("User-Agent", "Guest")
    return f"Hello, {user_agent}!"
@query.field("getusers")
def get_users(_,info):
    return User.query.all()

@mutation.field("user")
def reslove_user(_,info, name):
    return User.query.filter_by(name=name).first()

@mutation.field("user_todo")
def reslove_todo_list(_,info,user_id):
    return TODO.query.filter_by(user_id= user_id).all()

@mutation.field("create_user")
def create_user(_,info,name):
    return User.create(name=name)

@mutation.field("create_todo")
def create_todo(_,info,title, time,description, user_id, isSuperUser):
    return TODO.create(user_id=user_id, isSuperUser=isSuperUser,time=time, title=title,description=description)

@mutation.field("create_todo_su")
def create_todo_su(_,info,title, time,description, isSuperUser,user_id, image):
    return TODO.create(user_id=user_id, time=time, isSuperUser=isSuperUser,title=title,description=description, image=image)
@mutation.field("update_user_to_su")
def update_user_to_su(_,info, name):
    # user = User.query.filter_by(name = name).update(isSuperUser = True)
    return User.update_isSuperUser(name=name)
