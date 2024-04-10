from itsdangerous import URLSafeSerializer
from flask import make_response, redirect, url_for, request
from dotenv import load_dotenv
from ..models.users import User
import os

def get_key():
    load_dotenv()
    key = os.getenv('KEY')
    return key

def get_user(name):
    return User.query.filter_by(name=name).first()

#Inicializace serializeru pomocí secret key
serializer = URLSafeSerializer(get_key())

#Funkce pro vytvoření cookie
def create_secure_cookie(username):
    #Data co se uloží do cookie
    data = {"username": username}
    #Zašifrování dat
    encrypted_data = serializer.dumps(data)
    #Přesměrování na GET metodu hlavní stránky
    response = make_response(redirect(url_for('main.main_get')))
    #Nastavení cookie s daty
    response.set_cookie("user_info", encrypted_data, httponly=True, samesite="Strict", secure=False)
    return response

#Funkce pro čtení z cookie
def read_secure_cookie():
    #Získání dat z cookie
    encrypted_data = request.cookies.get("user_info")
    #Když jsou v cookie data tak se je pokusíme dešifrovat a max. věkem 1 hodina
    if encrypted_data:
        try:
            data = serializer.loads(encrypted_data, max_age=3600)
            return data
        except:
            pass
    return None

#Funkce pro vymazání cookie a návrat na login page - odhlášení
def delete_secure_cookie():
    response = make_response(redirect(url_for("main.main_get")))
    response.set_cookie("user_info", expires=0)
    return response

def get_current_user():
    cookie = read_secure_cookie()
    if cookie:
        username = cookie["username"]
        if username and get_user(username):
            return get_user(username)
        else:
            return None
    return None

