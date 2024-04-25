from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class EditPassword(FlaskForm):
    st_password = PasswordField('пароль старый', validators=[DataRequired()])
    password = PasswordField('Пароль новый', validators=[DataRequired()])
    password_again = PasswordField('Повторите новый пароль', validators=[DataRequired()])
    submit = SubmitField('заменить')
