from flask import request, render_template, session, redirect, url_for, g
from werkzeug.security import generate_password_hash
from app.models.user_model import UserModel
from app import db


def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # Récupérer les données du formulaire
        data = request.form
        username = data['username']
        password = data['password']
        print('data', data['username'], data['password'])

        # Vérifier si l'utilisateur existe déjà
        existing_user = UserModel.query.filter_by(username=username).first()

        if existing_user:
            return render_template('register.html', message='Ce nom d\'utilisateur existe déjà')

        # Créer un nouvel utilisateur
        hashed_password = generate_password_hash(password)
        new_user = UserModel(username=username, password_hash=hashed_password)

        # Ajouter l'utilisateur à la base de données
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))


def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # Récupérer les données du formulaire
        data = request.form
        username = data['username']
        password = data['password']
        print('data', data['username'], data['password'])

        # # Vérifier si l'utilisateur existe déjà
        existing_user = UserModel.query.filter_by(username=username).first()

        if not existing_user:
            return render_template('login.html', message='aucun utilisateur trouvé')

        # Vérifier si le mot de passe est correct
        if not existing_user.check_password(password):
            return render_template('login.html', message='mot de passe incorrect')

        # Stocker l'id de l'utilisateur dans la session
        session['user_id'] = existing_user.id

        return redirect(url_for('home'))


def logout():
    session.clear()
    return redirect(url_for('home'))