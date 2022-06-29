from flask_wtf import FlaskForm
from datetime import date
from wtforms import Form, PasswordField, StringField, TextAreaField, IntegerField, BooleanField, RadioField, SubmitField, validators
from wtforms.validators import InputRequired, Length, EqualTo, Email, ValidationError
from wtforms.fields import DateField


class RegistrationForm(FlaskForm):
    
    user_fname = StringField('First name', [validators.InputRequired(), validators.Length(min=1, max=25)])
    user_lname = StringField('Last name', [validators.InputRequired(), validators.Length(min=1, max=25)])
    email =StringField('Email address', [validators.InputRequired(), validators.Length(min=10, max=30), validators.Email(message='Not a valid email address.')])
    password = PasswordField('New password', [validators.InputRequired(), validators.Length(min=3, max=15), validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Confirm password')
    submit = SubmitField('Signup')


class GreetUserForm(FlaskForm):

    email = StringField('Email address', validators=[InputRequired(message = 'Enter your email'), 
                            Length(min=10, max=20), 
                            Email(message='Not a valid email address.')])
    password = StringField('Password', validators=[InputRequired(), 
                            Length(min=8, max=20, message='Enter the password associated with your account.')])
    submit = SubmitField('Login')


class SearchActivities(FlaskForm):

    search_location = StringField('City or zip', [validators.InputRequired(), validators.Length(min=2, max=25)])
    submit = SubmitField('Search city or zipcode')


class NewItinerary(FlaskForm):

    itin_name = StringField('Name your trip!', [validators.InputRequired(), validators.Length(min=2, max=30)])
    itin_location = StringField('What city are you visiting?', [validators.InputRequired(), validators.Length(min=2, max=20)])
    itin_start = DateField('Trip start date:', default=date.today)
    itin_end = DateField('Trip end date:', default=date.today)