from flask import Flask, render_template, url_for, redirect, flash
import os
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.google import make_google_blueprint

from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import (UserMixin, login_required, logout_user, LoginManager, login_user, current_user)

from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "scrfanfaklfetkey")
app.config["FB_CLIENT_ID"] = os.environ.get("FB_CLIENT_ID")
app.config["FB_CLIENT_SECRET"] = os.environ.get("FB_CLIENT_SECRET")

app.config["GOOGLE_CLIENT_ID"] = os.environ.get("GOOGLE_CLIENT_ID")
app.config["GOOGLE_CLIENT_SECRET"] = os.environ.get("GOOGLE_CLIENT_SECRET")


# set to 1 while still in development or else "insecure http message"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/daisy/wikiFam/backend/login.db'

# for Facebook
facebook_blueprint = make_facebook_blueprint(client_id="---", client_secret="---")
app.register_blueprint(facebook_blueprint, url_prefix="/auth/facebook/wikifam")

# for Google
google_blueprint = make_google_blueprint(client_id="---", client_secret="---", scope=['https://www.googleapis.com/auth/userinfo.email', 'openid', 'https://www.googleapis.com/auth/userinfo.profile'])
app.register_blueprint(google_blueprint, url_prefix="/auth")

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.String(250), primary_key=True)
    name = db.Column(db.String(250), unique=False)
    email = db.Column(db.String(250), unique=True)

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.String(250), db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get((user_id))

# For Facebook
facebook_blueprint.storage = SQLAlchemyStorage(OAuth, db.session, user=current_user)

@oauth_authorized.connect_via(facebook_blueprint)
@app.route('/name', methods=['POST'])
def getUser():
    return current_user.name

@oauth_authorized.connect_via(facebook_blueprint)
@app.route('/id')
def getUserId():
    return current_user.id


@oauth_authorized.connect_via(facebook_blueprint)
def facebookLoggedIn(blueprint, token):
    if not token:
        print("Failed to log in with FB")
        return False

    accInfo = blueprint.session.get('/me?fields=id,name,email')
    print(accInfo.json())

    # authorization went OK, no errors
    if not accInfo.ok:
        return False

    accInfoJson = accInfo.json()
    user_id = accInfoJson["id"]

    # find auth token in DBor create
    query = OAuth.query.filter_by(provider=blueprint.name, user_id=user_id)

    try:
        oauth = query.one()
        print(oauth)
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, user_id=user_id, token=token)

    if oauth.user:
        login_user(oauth.user)

    else:
        # create local user
        user = User(name=accInfoJson["name"], id=accInfoJson["id"], email=accInfoJson["email"])
        
        oauth.user = user
        
        db.session.add_all([user, oauth])
        db.session.commit()
        
        login_user(user)
        print("success logged in")

    print("curr user is ")
    print(current_user)

    return False

# notify on OAuth provider error
@oauth_error.connect_via(facebook_blueprint)
def facebook_error(blueprint, message, response):
    print("error oauth")

# For Google
google_blueprint.storage = SQLAlchemyStorage(OAuth, db.session, user=current_user)

@oauth_authorized.connect_via(google_blueprint)
def googleLoggedIn(blueprint, token):
    print("google login stuff")
    print(url_for("google.login"))

    if not blueprint.authorized: 
        return redirect(url_for("google.login"))
    if not token:
        print("Failed to log in with Google")
        return False

    accInfo = blueprint.session.get('/oauth2/v1/userinfo')

    print("person info is: ")
    print(accInfo.json())

    # authorization went OK, no errors
    if not accInfo.ok:
        return False

    accInfoJson = accInfo.json()
    user_id = accInfoJson["id"]

    # find auth token in DBor create
    query = OAuth.query.filter_by(provider=blueprint.name, user_id=user_id)

    try:
        oauth = query.one()
        print(oauth)
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, user_id=accInfoJson["id"], token=token)

    if oauth.user:
        login_user(oauth.user)

    else:
        # create local user
        user = User(name = accInfoJson["name"], id=accInfoJson["id"], email=accInfoJson["email"])
        
        oauth.user = user
        
        db.session.add_all([user, oauth])
        db.session.commit()
        
        login_user(user)
        print("success logged in")

    print("curr user is ")
    print(current_user)

    return False

# notify on OAuth provider error
@oauth_error.connect_via(facebook_blueprint)
def google_error(blueprint, message, response):
    print("error oauth")

@app.route("/")
@app.route("/login")
def idx():
    return redirect('http://localhost:5000')
    # return render_template("temp.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    print("logged out")
    flash("You have logged out")

    return redirect(url_for('idx'))

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True, port=3000)