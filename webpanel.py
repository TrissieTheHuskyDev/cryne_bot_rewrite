#Oauth2 code from https://github.com/discordapp/discord-oauth2-example

import os
from flask import Flask, g, session, redirect, request, url_for, jsonify, abort, render_template, flash
from requests_oauthlib import OAuth2Session
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField

from sql import  get_servers

from helper import hasPerm

########################################################################################################################

OAUTH2_CLIENT_ID = os.environ['OAUTH2_CLIENT_ID']
OAUTH2_CLIENT_SECRET = os.environ['OAUTH2_CLIENT_SECRET']
OAUTH2_REDIRECT_URI = 'http://localhost:5000/callback'

API_BASE_URL = os.environ.get('API_BASE_URL', 'https://discordapp.com/api')
AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


def token_updater(token):
    session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)


@app.route('/')
def index():
    scope = request.args.get(
        'scope',
        'identify guilds')
    discord = make_session(scope=scope.split(' '))
    authorization_url, state = discord.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth2_state'] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    if request.values.get('error'):
        return request.values['error']
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token
    return redirect(url_for('.me'))


@app.route('/me')
def me():
    print(get_servers())
    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()

    valid_guilds = []
    for guild in guilds:
        if hasPerm(guild["permissions"], 8):
            valid_guilds.append(guild)

    more_valid_guilds = []

    for gld in valid_guilds:
        for server in get_servers():
            for key in server.keys():
                if str(key) == gld["id"]:
                    more_valid_guilds.append(gld)
    global showable_guilds
    showable_guilds = []

    for srv in more_valid_guilds:
        showable_guilds.append((srv["name"], srv["name"]))

    print(showable_guilds)



    return jsonify(user=user, guilds=more_valid_guilds)

########################################################################################################################

class SettingsformForm(FlaskForm):

    showable_guilds = []
    def set_guilds(self, guilds):
        print("Class:")
        self.showable_guilds = guilds
        print(guilds)
        print(self.showable_guilds)

    msg = "Bitte fülle dieses Feld aus"
    logchid = StringField(validators=[validators.DataRequired(msg)],
                          render_kw={"placeholder": "ID des Nachrichtenlogchannels"})
    botcchid = StringField(validators=[validators.DataRequired(msg)],
                           render_kw={"placeholder": "ID des Botcommand-Channels"})
    remoj = StringField("Reaktions-Emoji für #beliebte-vorschläge", validators=[validators.DataRequired(msg)],
                        render_kw={"placeholder": "Reaktions-Emoji für #beliebte-vorschläge"})
    rcount = StringField("Anzahl von Reaktionen für #beliebte-vorschläge", validators=[validators.DataRequired(msg)],
                         render_kw={"placeholder": "Anzahl von Reaktionen für #beliebte-vorschläge"})
    belvchid = StringField(validators=[validators.DataRequired(msg)],
                           render_kw={"placeholder": "ID des #beliebte-vorschläge Channels"})
    banmsgch = StringField(validators=[validators.DataRequired(msg)],
                           render_kw={"placeholder": "ID des Channels für Banmeldungen"})
    leavemsgch = StringField(validators=[validators.DataRequired(msg)],
                             render_kw={"placeholder": "ID des Channels für Leavemeldungen"})
    kickmsgch= StringField(validators=[validators.DataRequired(msg)],
                           render_kw={"placeholder": "ID des Channels für Kickmeldungen"})
    rcmsgch = StringField(validators=[validators.DataRequired(msg)],
                          render_kw={"placeholder": "ID des Channels für Rollenänderungesmeldungen"})
    adminrole = StringField(validators=[validators.DataRequired(msg)],
                            render_kw={"placeholder": "Name der Administratorrolle"})
    roleonjoin = StringField(validators=[validators.DataRequired(msg)],
                             render_kw={"placeholder": "ID der Rolle, die Nutzern beim Joinen zugewiesen wird"})
    rssurl = StringField(validators=[validators.DataRequired(msg)],
                         render_kw={"placeholder": "URL des RSS-Feeds"})
    servers = SelectField(validators=[validators.DataRequired(msg)],choices=showable_guilds)

    submit = SubmitField("Send")

########################################################################################################################
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), category="failure")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    SettingsformForm.set_guilds(showable_guilds)
    form = SettingsformForm()
    if request.method == 'POST':
        if form.validate():
            flash("Die Einstellungen wurden erfolgreich geändert", category="success")
            return render_template('settings.html', form=form)
        else:
            flash_errors(form)
        return render_template('settings.html', form=form)
    elif request.method == 'GET':

        return render_template('settings.html', form=form)

########################################################################################################################

if __name__ == '__main__':
    app.run()