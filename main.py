from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm, AddCafeForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)


#Migrate to add new column to table that exist
# migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    cafes = relationship("Cafe", back_populates="author")


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    map_url = db.Column(db.String(500))
    img_url = db.Column(db.String(500))
    location = db.Column(db.String(250))
    has_sockets = db.Column(db.Boolean)
    has_toilet = db.Column(db.Boolean)
    has_wifi = db.Column(db.Boolean)
    can_take_calls = db.Column(db.Boolean)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="cafes")


db.create_all()


@app.route('/')
def get_all_cafes():
    cafes = Cafe.query.all()
    return render_template("index.html", all_cafes=cafes)


@app.route("/cafe/<int:cafe_id>", methods=["GET", "POST"])
def show_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    return render_template("cafe.html", cafe=cafe)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_cafes'))

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("get_all_cafes"))

    return render_template("register.html", form=form)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():

        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for("get_all_cafes"))

    return render_template("add_cafe.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return render_template("logout.html")


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run()