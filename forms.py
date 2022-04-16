from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForms

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class AddCafeForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    map_url = StringField("Map", validators=[DataRequired(), URL()])
    img_url = StringField("Image", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Sockets")
    has_toilet = BooleanField("Toilet")
    has_wifi = BooleanField("Wifi")
    can_take_calls = BooleanField("Calls")
    seats = IntegerField("Seats", validators=[DataRequired()])
    coffee_price = FloatField("Price", validators=[DataRequired()])
    #author_id = IntegerField("Author id", validators=[DataRequired()])
    submit = SubmitField("Submit cafe")