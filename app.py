from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


db = SQLAlchemy()

app.secret_key = "secret-key"

#conn = 'postgresql://postgres:2003@localhost:5432/testflask'

conn = 'sqlite:///testflask.db'

app.config['SQLALCHEMY_DATABASE_URI'] = conn

app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/inscription')
def signup():
    return render_template('inscription.html')


@app.route('/accueil')
def accueil():
    return render_template('index.html')


@app.route('/connexion')
def login():
    return render_template('connexion.html')


@app.route('/deconnexion')
def logout():
    return render_template('index.html')


@app.route('/connexion', methods=['GET', 'POST'])
def verify():
    vrf_email = request.form['email']
    vrf_password = request.form['password']
    user = User.query.filter_by(email=vrf_email).first()

    if user and user.password == vrf_password:
        return redirect('/logged')
    else:
        flash("votre email ou votre mot de passe ne correspond pas")
        return redirect('/connexion')


@app.route('/logged')
def logged():
    return render_template('logged.html')


@app.route('/inscription', methods=['GET', 'POST'])
def insert():
    nom = request.form['nom']
    prenom = request.form['prenom']
    email = request.form['email']
    password = request.form['password']
    password_conf = request.form['password_conf']
    user = User.query.filter_by(email=email).first()

    if user:
        flash("cet email est déja utilisé")
        return redirect('/inscription')
    elif password != password_conf:
        flash("les mot de passe ne correspondent pas")
        return redirect('/inscription')
    else:
        user_add = User(nom=nom, prenom=prenom, email=email, password=password)
        db.session.add(user_add)
        db.session.commit()
        nom = session.get('nom')
        return render_template('inscris.html', nom=nom)


def create_database(app):
    db.create_all(app=app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
