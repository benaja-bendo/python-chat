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

        # Vérifier si l'utilisateur existe déjà
        existing_user = UserModel.query.filter_by(username=username).first()

        if not existing_user:
            return render_template('login.html', message='aucun utilisateur trouvé')

        # Vérifier si le mot de passe est correct
        if not existing_user.check_password(password):
            return render_template('login.html', message='mot de passe incorrect')

        # Stocker l'id et le nom d'utilisateur de l'utilisateur dans la session
        session['user_id'] = existing_user.id
        session['username'] = existing_user.username

        return redirect(url_for('home'))

def show_messages():
    # Récupérer l'id et le nom d'utilisateur de l'utilisateur actuel depuis la session
    user_id = session.get('user_id')
    username = session.get('username')

    # Utiliser ces informations pour afficher les messages dans le bon format
    messages = get_messages_for_user(user_id)  # Remplacez ceci par votre logique de récupération des messages

    # Passez ces informations au modèle HTML
    return render_template('messages.html', messages=messages, current_user_id=user_id, current_username=username)

def logout():
    session.clear()
    return redirect(url_for('home'))