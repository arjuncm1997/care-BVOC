from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from health.models import  *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import SelectField




class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')   

    def validate_email(self, email):
        user = Login.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Login.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Login.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class Imageform(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=40)])
    pic = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')


class Creditcard(FlaskForm):
    name = StringField('Name',render_kw={"placeholder":"Name"},
                        validators=[DataRequired()])
    number = IntegerField('number',render_kw={"placeholder":".... .... .... ...."},validators=[DataRequired()])
    cvv = IntegerField(' cvv',render_kw={"placeholder":"..."},
                        validators=[DataRequired()])
    date = StringField('date',render_kw={"placeholder":"MM/YY"},
                        validators=[DataRequired()])
    submit = SubmitField('Make A Payment')

class Paypal(FlaskForm):
    number = IntegerField('number',render_kw={"placeholder":"xxxx xxxx xxxx xxxx"},
                        validators=[DataRequired()])
    name = StringField('Name',render_kw={"placeholder":"Name"},validators=[DataRequired()])
    cvv = IntegerField(' cvv',render_kw={"placeholder":"xxx"},
                        validators=[DataRequired()])
    date = StringField('date',render_kw={"placeholder":"MM/YY"},
                        validators=[DataRequired()])
    submit = SubmitField('Proceed Payment')



class Amountform(FlaskForm):
    amount = StringField('Amount',render_kw={"placeholder":"...."},
                        validators=[DataRequired()])
    submit = SubmitField('Proceed Payment')


class DocterForm(FlaskForm):
    name = StringField('Username',render_kw={"placeholder":"name"},
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',render_kw={"placeholder":"email"},
                        validators=[DataRequired(), Email()])
    age = IntegerField('Age',render_kw={"placeholder":"age"},
                           validators=[DataRequired()])
    quali = StringField('Qualification',render_kw={"placeholder":"qualification"},validators=[DataRequired(), Length(min=2, max=30)])
    speci = StringField('Specilized Area',render_kw={"placeholder":"specilized area"},validators=[DataRequired(), Length(min=2, max=30)])
    doctype = StringField('DocterType',render_kw={"placeholder":"docterType"},validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Submitt')

    def validate_username(self, username):
        user = Login.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Login.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class StaffForm(FlaskForm):
    name = StringField('Username',render_kw={"placeholder":"name"},
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',render_kw={"placeholder":"email"},
                        validators=[DataRequired(), Email()])
    age = IntegerField('Age',render_kw={"placeholder":"age"},
                           validators=[DataRequired()])
    quali = StringField('Qualification',render_kw={"placeholder":"qualification"},validators=[DataRequired(), Length(min=2, max=30)])
    exp = StringField(' Experience',render_kw={"placeholder":"experience"},validators=[DataRequired(), Length(min=2, max=30)])
    add = StringField('Address',render_kw={"placeholder":"address"},validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Submitt')

    def validate_username(self, username):
        user = Login.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Login.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class StaffeditForm(FlaskForm):
    name = StringField('Username',render_kw={"placeholder":"name"},
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',render_kw={"placeholder":"email"},
                        validators=[DataRequired(), Email()])
    age = IntegerField('Age',render_kw={"placeholder":"age"},
                           validators=[DataRequired()])
    quali = StringField('Qualification',render_kw={"placeholder":"qualification"},validators=[DataRequired(), Length(min=2, max=30)])
    exp = StringField(' Experience',render_kw={"placeholder":"experience"},validators=[DataRequired(), Length(min=2, max=30)])
    add = StringField('Address',render_kw={"placeholder":"address"},validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Submitt')


class DoctereditForm(FlaskForm):
    name = StringField('Username',render_kw={"placeholder":"name"},
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',render_kw={"placeholder":"email"},
                        validators=[DataRequired(), Email()])
    age = IntegerField('Age',render_kw={"placeholder":"age"},
                           validators=[DataRequired()])
    quali = StringField('Qualification',render_kw={"placeholder":"qualification"},validators=[DataRequired(), Length(min=2, max=30)])
    speci = StringField('Specilized Area',render_kw={"placeholder":"specilized area"},validators=[DataRequired(), Length(min=2, max=30)])
    doctype = StringField('DocterType',render_kw={"placeholder":"docterType"},validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Submitt')


class Accountform(FlaskForm):
    name = StringField('Username',
                           validators=[ Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Email()])
    pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class Accountformstaff(FlaskForm):
    name = StringField('Username',
                           validators=[ Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Email()])
    pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    age = IntegerField('Age',render_kw={"placeholder":"age"},
                           validators=[DataRequired()])
    quali = StringField('Qualification',render_kw={"placeholder":"qualification"},validators=[DataRequired(), Length(min=2, max=30)])
    exp = StringField(' Experience',render_kw={"placeholder":"experience"},validators=[DataRequired(), Length(min=2, max=30)])
    add = StringField('Address',render_kw={"placeholder":"address"},validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update')


class Accountformdocter(FlaskForm):
    name = StringField('Username',
                           validators=[ Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Email()])
    pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    age = IntegerField('Age',render_kw={"placeholder":"age"},
                           validators=[DataRequired()])
    quali = StringField('Qualification',render_kw={"placeholder":"qualification"},validators=[DataRequired(), Length(min=2, max=30)])
    speci = StringField(' Experience',render_kw={"placeholder":"experience"},validators=[DataRequired(), Length(min=2, max=30)])
    dtype = StringField('Address',render_kw={"placeholder":"address"},validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update')


class Changepassword(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[ EqualTo('password')])
    submit = SubmitField('Reset Password')

class Reset(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = Login.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')