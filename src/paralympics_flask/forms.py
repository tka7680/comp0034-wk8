from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField, StringField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from paralympics_flask import db
from paralympics_flask.models import Region


def get_countries():
    return db.session.execute(db.select(Region).order_by(Region.region)).scalars()


class EventForm(FlaskForm):
    # the names of the fields exactly match the attributes of the Event class for convenience
    # Drop down selection with options specified in the form class.
    type = SelectField('Event type', choices=[('summer', 'Summer'), ('winter', 'Winter')], validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), ], render_kw={"placeholder": 2020})
    # Select the country from a dropdown list based on the Region table.
    # Uses WTForms-SQLAlchemy https://wtforms-sqlalchemy.readthedocs.io/en/latest/wtforms_sqlalchemy/
    country = QuerySelectField('Country', query_factory=get_countries, get_label='region')
    # 'NOC' is a foreign key determined by country, this will be determined in the route code
    # Alternate validation syntax, see https://wtforms.readthedocs.io/en/3.1.x/fields/#field-definitions
    host = StringField('Host city', [validators.optional()])
    start = DateField('Start date', [validators.data_required()])
    end = DateField('End date', [validators.data_required()])
    # 'duration' is omitted as this will be calculated in the route code when saved to the database
    disabilities_included = SelectMultipleField('Disabilities included',
                                                choices=[('Spinal injury', 'Spinal injury'), ('Amputee', 'Amputee'),
                                                         ('Vision Impairment', 'Vision Impairment'),
                                                         ('Cerebral Palsy', 'Cerebral Palsy'),
                                                         ('Les Autres', 'Les Autres'),
                                                         ('Intellectual Disability', 'Intellectual Disability')])
    countries = IntegerField('Total number of participating countries', [validators.optional()])
    events = IntegerField('Total number of events', [validators.optional()])
    sports = IntegerField('Total number of sports', [validators.optional()])
    participants_m = IntegerField('Total number of male participants', [validators.optional()])
    participants_f = IntegerField('Total number of female participants', [validators.optional()])
    participants = IntegerField('Total number of participants', [validators.optional()])
    highlights = TextAreaField('Highlights', [validators.optional(), validators.length(max=200)])

    # 'NOC' is a foreign key determined by country, this will be added in the route code
    # 'duration' will be calculated in the route code