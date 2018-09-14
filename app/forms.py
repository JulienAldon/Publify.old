#!/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class UserNameForm(FlaskForm):
    username = StringField('Spotify Username', validators=[DataRequired()])
    submit = SubmitField('Start')

class MyForm(FlaskForm):
    sync = SubmitField('Synchronize')
