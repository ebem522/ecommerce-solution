from flask_wtf import FlaskForm/Users/SapunNgoensritong/Documents/GitHub/ecommerce-solution/forms.py
from wtforms import StringField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])

