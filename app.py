from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
import os

import json

# Abre el archivo JSON
with open('creds_google.json') as f:
    # Lee el contenido del archivo
    data = json.load(f)

# Accede a los valores del archivo JSON
dic = data['web']
client_id = dic['client_id']
client_secret = dic['client_secret']
access_token_url = dic['token_uri']
authorize_url = dic['auth_uri']
redirect_uri = dic['redirect_uris']
print(redirect_uri)

# Imprime los valores leídos
#print("Client ID:", client_id)
#print("Client Secret:", client_secret)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configurar OAuth con Google
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=client_id,
    client_secret=client_secret,
    access_token_url=access_token_url,
    access_token_params=None,
    authorize_url= authorize_url,
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/')
def index():
    email = session.get('email', None)
    return f'Hola, {email}!'

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['email'] = user_info['email']
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
