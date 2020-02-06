import os

import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow

# OAuth2.0 details
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['email']
API_SERVICE_NAME = ''
API_VERSION = 'v2'

app = flask.Flask(__name__)
app.secret_key = 'REPLACE ME - this value is here as a placeholder.'

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

@app.route('/')
def main():
    if 'credentials' not in flask.session:
        return flask.render_template('home.html', title='Home', user=None)

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials']
    )
    flask.session['credentials'] = credentials_to_dict(credentials)
    return flask.render_template('home.html', title='Home', user='test')

@app.route('/login')
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    flask.session['state'] = state

    return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state
    )
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect('/')

@app.route('/logout')
def logout():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return flask.redirect('/')

@app.route('/public/<path:path>')
def public(path):
    return flask.send_from_directory('public', path)

@app.route('/resources/<path:path>')
def resources(path):
    return flask.send_from_directory('public/resources', path)

if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '0'
    app.run('localhost', 8080, debug=True)
