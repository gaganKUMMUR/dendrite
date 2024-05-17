import requests

BASE_URL = f"http://127.0.0.1:8000/"


def get_users_list():
    body = """query{getusers{id,name,isSuperUser}}"""
    resp = requests.post(BASE_URL, json={"query": body}).json()
    lst = []
    for users in resp['data']['getusers']:
        lst.append(users['name'])
    return lst
def get_user_status(name):
    body = """mutation{user(name:"%s"){id, isSuperUser}}""" % (name)
    resp = requests.post(BASE_URL, json={"query": body}).json()
    return resp['data']['user']['isSuperUser']

def get_user_id(name):
    body = """mutation{user(name:"%s"){id, isSuperUser}}""" % (name)
    resp = requests.post(BASE_URL, json={"query": body}).json()
    return resp['data']['user']['id']
def create_user(name):
    body = """mutation{create_user(name:"%s"){id,name,isSuperUser}}""" %(name)
    resp = requests.post(BASE_URL, json={"query": body})
    return resp.text
def update_user_to_su(name):
    body = """mutation{update_user_to_su(name:"%s"){id, name, isSuperUser}}""" %(name)
    resp = requests.post(BASE_URL, json={"query": body}).json()
def create_todo_grp(user_id, title, time, description):
    body = """mutation{create_todo(user_id:%d,time:"%s",title:"%s",description:"%s"){id}}""" %(user_id,time,title,description)
    resp = requests.post(BASE_URL, json={"query": body}).json()
    return resp['data']['create_todo']['id']
def create_todo_su_grp(id, image):
    body = """mutation{create_todo_su(id:%d,image:"%s"){id,isSuperUser}}""" %(id,image)
    resp = requests.post(BASE_URL, json={"query": body}).json()
    return resp['data']['create_todo_su']['isSuperUser']

def user_todos(user_id):
    body = """mutation{user_todo(user_id:%d){id,image,isSuperUser,title,description,time}}"""%(user_id)
    resp = requests.post(BASE_URL, json={"query": body}).json()
    return resp['data']['user_todo']
def update_todo(id, time,title,description):
    body = """mutation{update_todo(id:%d,time:"%s",title:"%s",description:"%s"){id, time,title}}"""%(id,time,title,description)
    resp = requests.post(BASE_URL, json={"query" : body})
    return resp.status_code

def delete_todo_api(id):
    body="""mutation{delete_todo(id:%d){id,title}}"""%(id)
    resp = requests.post(BASE_URL,json={"query":body})
    return resp.status_code
if __name__ == "__main__":
    resp = user_todos(2)
    print(resp)
    