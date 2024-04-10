from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp
import requests
from ..service.cookies import get_current_user
from ..models.locations import Location
from ..service.database import db
from ..service.weather import current_location

from ..service.weather import show_weather

main_bp = Blueprint('main', __name__)

class MainForm(FlaskForm):
    city = StringField("Location", validators=[InputRequired()], render_kw={"placeholder": "Location"})
    submit = SubmitField("Find")

class PayForm(FlaskForm):
    card = StringField("Číslo karty", validators=[
        InputRequired(message="Číslo karty je povinné pole."),
        Length(min=16, max=16, message="Číslo karty musí mít 16 číslic."),
        Regexp('^[0-9]*$', message="Číslo karty může obsahovat pouze číslice.")
    ], render_kw={"placeholder": "XXXX XXXX XXXX XXXX"})
    btn1 = SubmitField("Month")
    btn2 = SubmitField("3 Month")
    btn3 = SubmitField("Year")

@main_bp.route('/', methods=['GET'])
def main_get():
    main_form = MainForm()
    location = request.args.get('location')
    #user_ip = request.remote_addr
    user_ip = '147.230.11.198'
    user = get_current_user()
    if location:
        weather, forecast, history, error, loc = show_weather(location)
        if error:
            return render_template('index.html', error, main_form=main_form, location=location, weather=weather, user=user, forecast=forecast, history=history)
        else:
            main_form.process()
            return render_template('index.html', weather=weather, main_form=main_form, user=user, forecast=forecast, history=history, location=location, fav=True)
    else:
        weather, forecast, history, error, city = current_location()
        if error:
            return render_template('index.html', error=error, main_form=main_form, location=city, weather=weather, user=user, forecast=forecast, history=history)
        else:
            main_form.process()
            return render_template('index.html', actual=True, location=city, weather=weather, main_form=main_form, user=user, forecast=forecast, history=history)
    

@main_bp.route('/', methods=['POST'])
def main_post():
    main_form = MainForm()
    user = get_current_user()
    if main_form.validate_on_submit():
        print('here2')
        city = main_form.city.data
        weather, forecast, history, error, loc = show_weather(city)
        print(weather, error)
        if error:
            return render_template('index.html', error=error, main_form=main_form, location=city, weather=weather, user=user, forecast=forecast, history=history)
        else:
            main_form.process()
            return render_template('index.html', weather=weather, main_form=main_form, user=user, forecast=forecast, location=city, history=history)
    return render_template('index.html', main_form=main_form, location=None, weather=None, user=user, forecast=None, history=None)

@main_bp.route('/payment', methods=['GET'])
def payment():
    user = get_current_user()
    pay_form = PayForm()
    if not user:
        return redirect(url_for('user.login'))
    
    return render_template('payment.html', user=user, pay_form=pay_form)

@main_bp.route('/payment', methods=['POST'])
def pay():
    pay_form = PayForm()
    user = get_current_user()
    if not user:
        return redirect(url_for('user.login'))
    
    if pay_form.validate_on_submit():
        if pay_form.btn1.data:
            months = 1
        elif pay_form.btn2.data:
            months = 3
        elif pay_form.btn3.data:
            months = 12
    user.set_premium(months)
    db.session.commit()

    return redirect(url_for('main.main_get'))

@main_bp.route('/addToFavourite')
def add_to_favourite():
    main_form = MainForm()
    location = (request.args.get('location'))
    user = get_current_user()
    if not user:
        return redirect(url_for('user.login'))

    try:
        new_location = Location(location, user)
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('main.main_get', location=location))
    except Exception as e:
        db.session.rollback()
        error_message = "Unable to add to favourite."
        return render_template('index.html', error=error_message, main_form=main_form, user = user)
