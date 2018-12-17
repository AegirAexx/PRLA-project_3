""" The validation class for the Folf App. It expands wtforms."""


from flask_wtf import FlaskForm
import re
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class RegistrationForm(FlaskForm):
    """ The validation rules for the Registration form."""

    # Each piece of data gets its own variable and set of rules to abide to.
    # A regular expression to validate the players name.
    pattern = re.compile('^[A-za-z]*[^.{}\[\]0-9]+[A-za-z]*$')
    name = StringField('Name', validators=[
                              DataRequired(),
                              Regexp(
                                  pattern, message='Only Alpha.'),
                              Length(max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('SIGN UP')


class LoginForm(FlaskForm):
    """ The validation rules for the Login form."""

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('LOGIN')


class ResetForm(FlaskForm):
    """ The validation rules for the Reset form."""

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('RESET')


class PlayGameForm(FlaskForm):
    """ The validation rules for the Play sheet form."""

    # A regular expression to validate the players name.
    pattern = re.compile('^[A-za-z]*[^.{}\[\]]+[A-za-z]*$')
    player_name = StringField('Player', validators=[
                              DataRequired(),
                              Regexp(
                                  pattern, message='Only Alphanumerics.'),
                              Length(max=25)])
    hole_1 = IntegerField('Hole 1', default=0)
    hole_2 = IntegerField('Hole 2', default=0)
    hole_3 = IntegerField('Hole 3', default=0)
    hole_4 = IntegerField('Hole 4', default=0)
    hole_5 = IntegerField('Hole 5', default=0)
    hole_6 = IntegerField('Hole 6', default=0)
    hole_7 = IntegerField('Hole 7', default=0)
    hole_8 = IntegerField('Hole 8', default=0)
    hole_9 = IntegerField('Hole 9', default=0)
    submit = SubmitField('SUBMIT')
