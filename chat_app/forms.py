import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError

from chat_app import db
from chat_app.models import User
from chat_app.max_field_len import max_field_len


class ExtendedFlaskForm(FlaskForm):
    def formatErrorString(self, message):
        message_length = len(message)
        max_field_length = max_field_len(self.errors)

        complete_string = ''
        for field, field_msgs in self.errors.items():
            field_spacing = ' ' * (max_field_length - len(field) + 1)
            field_key = f'{field}:{field_spacing}'
            field_values = f"\n{' ' * message_length}{' ' *
                                                      len(field_key)}".join(field_msgs)

            complete_string += f'{field_key}{field_values}\n{' ' *
                                                             message_length}'

        return f'{message}{complete_string}'.rstrip()


class LoginForm(ExtendedFlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(
        "The pattern does not match the syntax of a regular email address")], render_kw={"placeholder": "Enter Email", "icon_class": "bi-envelope-at-fill"})

    password = PasswordField('Password', validators=[DataRequired(), Regexp(
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&=+\-_])[A-Za-z\d@$!%*?&=+\-_]{8,}$', message="The string does not correctly match the pattern")], render_kw={"placeholder": "Enter Password", "icon_class": "bi-lock-fill"})

    submit = SubmitField("Sign In")


class SignupForm(ExtendedFlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp(
        r'^(?=.{2,14}$)(?!.*[ _-]{2})[a-zA-Z](?!.*[ _-]$)[a-zA-Z0-9]*[ _-]?[a-zA-Z0-9]+$', message="The string does not correctly match the pattern"
    )], render_kw={"placeholder": "Enter username", "icon_class": "bi-person-fill"})

    email = EmailField("Email", validators=[DataRequired(), Email("The pattern does not match the syntax of a regular email address")], render_kw={
                       "placeholder": "Enter Email", "icon_class": "bi-envelope-at-fill"})

    password = PasswordField('Password', validators=[DataRequired(), Regexp(
        r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&=+\-_])[A-Za-z\d@$!%*?&=+\-_]{8,16}$', message="The string does not correctly match the pattern"), EqualTo("confirm_pwd", message="Passwords must match")], render_kw={"placeholder": "Enter Password", "icon_class": "bi-lock-fill"})

    confirm_pwd = PasswordField('Conifrm password', render_kw={
                                "placeholder": "Conifrm password", "icon_class": "bi-lock-fill"})

    submit = SubmitField("Sign up")

    def validate_email(self, email):
        user = db.session.scalar(
            sa.select(User).where(User.email == email.data))

        if user is not None:
            raise ValidationError('Please use a different email address.')
        
        return user