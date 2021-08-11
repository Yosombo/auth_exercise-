
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from wtforms_alchemy import model_form_factory
from models import User, db
BaseModelForm = model_form_factory(FlaskForm)

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

# class ModelForm(BaseModelForm):
#     @classmethod
#     def get_session(self):
#         return db.session


# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         include_primary_keys = True
