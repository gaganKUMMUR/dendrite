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
if __name__ == "__main__":
    resp = create_user("gagan3")
    print(resp)
    