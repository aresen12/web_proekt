from flask_wtf import FlaskForm
from wtforms import FormField, StringField, SubmitField, FieldList
from wtforms.validators import DataRequired


class ZakForm(FlaskForm):
    to_location = StringField('Введите свой адрес', validators=[DataRequired()])
     # ss = FieldList("CDEK", "Почта России", validators=[DataRequired()])
    submit = SubmitField('рассчитать')
