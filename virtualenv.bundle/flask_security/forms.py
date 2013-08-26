# -*- coding: utf-8 -*-
"""
    flask.ext.security.forms
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Flask-Security forms module

    :copyright: (c) 2012 by Matt Wright.
    :license: MIT, see LICENSE for more details.
"""

import inspect
import urlparse

import flask_wtf as wtf

from flask import request, current_app
from flask_wtf import Form as BaseForm
from wtforms import TextField, PasswordField, validators, \
    SubmitField, HiddenField, BooleanField, ValidationError, Field
from flask_login import current_user
from werkzeug.local import LocalProxy

from .confirmable import requires_confirmation
from .utils import verify_and_update_password, get_message

# Convenient reference
_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)

_default_field_labels = {
    'email': 'Email Address',
    'password': 'Password',
    'remember_me': 'Remember Me',
    'login': 'Login',
    'retype_password': 'Retype Password',
    'register': 'Register',
    'send_confirmation': 'Resend Confirmation Instructions',
    'recover_password': 'Recover Password',
    'reset_password': 'Reset Password',
    'retype_password': 'Retype Password',
    'new_password': 'New Password',
    'change_password': 'Change Password',
    'send_login_link': 'Send Login Link'
}


class ValidatorMixin(object):
    def __call__(self, form, field):
        if self.message and self.message.isupper():
            self.message = get_message(self.message)[0]
        return super(ValidatorMixin, self).__call__(form, field)


class EqualTo(ValidatorMixin, validators.EqualTo):
    pass


class Required(ValidatorMixin, validators.Required):
    pass


class Email(ValidatorMixin, validators.Email):
    pass


class Length(ValidatorMixin, validators.Length):
    pass


email_required = Required(message='EMAIL_NOT_PROVIDED')
email_validator = Email(message='INVALID_EMAIL_ADDRESS')
password_required = Required(message='PASSWORD_NOT_PROVIDED')
password_length = Length(min=6, max=128, message='PASSWORD_INVALID_LENGTH')


def get_form_field_label(key):
    return _default_field_labels.get(key, '')


def unique_user_email(form, field):
    if _datastore.find_user(email=field.data) is not None:
        msg = get_message('EMAIL_ALREADY_ASSOCIATED', email=field.data)[0]
        raise ValidationError(msg)


def valid_user_email(form, field):
    form.user = _datastore.find_user(email=field.data)
    if form.user is None:
        raise ValidationError(get_message('USER_DOES_NOT_EXIST')[0])


class Form(BaseForm):
    def __init__(self, *args, **kwargs):
        if current_app.testing:
            self.TIME_LIMIT = None
        super(Form, self).__init__(*args, **kwargs)


class EmailFormMixin():
    email = TextField(
        get_form_field_label('email'),
        validators=[email_required, email_validator])


class UserEmailFormMixin():
    user = None
    email = TextField(
        get_form_field_label('email'),
        validators=[email_required, email_validator, valid_user_email])


class UniqueEmailFormMixin():
    email = TextField(
        get_form_field_label('email'),
        validators=[email_required, email_validator, unique_user_email])


class PasswordFormMixin():
    password = PasswordField(
        get_form_field_label('password'), validators=[password_required])


class NewPasswordFormMixin():
    password = PasswordField(
        get_form_field_label('password'),
        validators=[password_required, password_length])


class PasswordConfirmFormMixin():
    password_confirm = PasswordField(
        get_form_field_label('retype_password'),
        validators=[EqualTo('password', message='RETYPE_PASSWORD_MISMATCH')])


class NextFormMixin():
    next = HiddenField()

    def validate_next(self, field):
        url_next = urlparse.urlsplit(field.data)
        url_base = urlparse.urlsplit(request.host_url)
        if url_next.netloc and url_next.netloc != url_base.netloc:
            field.data = ''
            raise ValidationError(get_message('INVALID_REDIRECT')[0])


class RegisterFormMixin():
    submit = SubmitField(get_form_field_label('register'))

    def to_dict(form):
        def is_field_and_user_attr(member):
            return isinstance(member, Field) and \
                hasattr(_datastore.user_model, member.name)

        fields = inspect.getmembers(form, is_field_and_user_attr)
        return dict((key, value.data) for key, value in fields)


class SendConfirmationForm(Form, UserEmailFormMixin):
    """The default forgot password form"""

    submit = SubmitField(get_form_field_label('send_confirmation'))

    def __init__(self, *args, **kwargs):
        super(SendConfirmationForm, self).__init__(*args, **kwargs)
        if request.method == 'GET':
            self.email.data = request.args.get('email', None)

    def validate(self):
        if not super(SendConfirmationForm, self).validate():
            return False
        if self.user.confirmed_at is not None:
            self.email.errors.append(get_message('ALREADY_CONFIRMED')[0])
            return False
        return True


class ForgotPasswordForm(Form, UserEmailFormMixin):
    """The default forgot password form"""

    submit = SubmitField(get_form_field_label('recover_password'))


class PasswordlessLoginForm(Form, UserEmailFormMixin):
    """The passwordless login form"""

    submit = SubmitField(get_form_field_label('send_login_link'))

    def __init__(self, *args, **kwargs):
        super(PasswordlessLoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        if not super(PasswordlessLoginForm, self).validate():
            return False
        if not self.user.is_active():
            self.email.errors.append(get_message('DISABLED_ACCOUNT')[0])
            return False
        return True


class LoginForm(Form, NextFormMixin):
    """The default login form"""

    email = TextField(get_form_field_label('email'))
    password = PasswordField(get_form_field_label('password'))
    remember = BooleanField(get_form_field_label('remember_me'))
    submit = SubmitField(get_form_field_label('login'))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        if self.email.data.strip() == '':
            self.email.errors.append(get_message('EMAIL_NOT_PROVIDED')[0])
            return False

        if self.password.data.strip() == '':
            self.password.errors.append(get_message('PASSWORD_NOT_PROVIDED')[0])
            return False

        self.user = _datastore.get_user(self.email.data)

        if self.user is None:
            self.email.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
            return False
        if not verify_and_update_password(self.password.data, self.user):
            self.password.errors.append(get_message('INVALID_PASSWORD')[0])
            return False
        if requires_confirmation(self.user):
            self.email.errors.append(get_message('CONFIRMATION_REQUIRED')[0])
            return False
        if not self.user.is_active():
            self.email.errors.append(get_message('DISABLED_ACCOUNT')[0])
            return False
        return True


class ConfirmRegisterForm(Form, RegisterFormMixin,
                          UniqueEmailFormMixin, NewPasswordFormMixin):
    pass


class RegisterForm(ConfirmRegisterForm, PasswordConfirmFormMixin):
    pass


class ResetPasswordForm(Form, NewPasswordFormMixin, PasswordConfirmFormMixin):
    """The default reset password form"""

    submit = SubmitField(get_form_field_label('reset_password'))


class ChangePasswordForm(Form, PasswordFormMixin):
    """The default change password form"""

    new_password = PasswordField(
        get_form_field_label('new_password'),
        validators=[password_required, password_length])

    new_password_confirm = PasswordField(
        get_form_field_label('retype_password'),
        validators=[EqualTo('new_password', message='RETYPE_PASSWORD_MISMATCH')])

    submit = SubmitField(get_form_field_label('change_password'))

    def validate(self):
        if not super(ChangePasswordForm, self).validate():
            return False

        if self.password.data.strip() == '':
            self.password.errors.append(get_message('PASSWORD_NOT_PROVIDED')[0])
            return False
        if not verify_and_update_password(self.password.data, current_user):
            self.password.errors.append(get_message('INVALID_PASSWORD')[0])
            return False
        return True
