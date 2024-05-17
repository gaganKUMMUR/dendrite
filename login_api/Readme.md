###Steps run login api###

1. Running KeyCloak
```docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:24.0.4 start-dev```
2. Login with credentials username = admin and password = admin
3. create realm named dendrite
4. create a client named dendrite_login
    a. In Capability config turn on Client authentication and check Implicit flow and Service accounts roles
    b. set root url to http://localhost:5000/
    c. set valid redirect uris to http://127.0.0.1:5000/authorize
    d. set web origin uri to http://localhost:5000/*
    e. save the client
4. in credential tab get client secrete key

Running flask app
1. pip3 install -r requirements.txt
2. change the client serect key in client_secret.json paste the key that you got from previous step.
3. python3 new_app.py (Note : api should be running)
