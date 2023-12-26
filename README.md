# Projet Python avec Flask et SQLite

Ce projet est un exemple d'application Python utilisant le framework Flask pour créer un serveur web et SQLite comme base de données.

## Installation

1. Clonez ce dépôt sur votre machine locale :

   ```sh
    git clone https://github.com/benaja-bendo/python-chat.git
   ```

2. Copier le fichier .env.example et renommé .env

   ```sh
   cp .env.example .env
   ```

3. Installez les dépendances du projet :

   ```bash
   pip install -r requirements.txt
   ```

4. Lancez le serveur de développement :

   ```bash
   python run.py
   ```

5. Ouvrez votre navigateur à l'adresse [http://localhost:5000](http://localhost:5000).

## Utilisation

Capture d'écran

## structure du projet

```md
python_chat/
│
├── app/
│ ├── **init**.py
│ ├── templates/
│ │ ├── base.html
│ │ ├── home.html
│ │ ├── login.html
│ │ ├── register.html
│ │ ├── private_message.html
│ ├── model/
│ │ ├── user_model.py
│ │ ├── message_model.py
│ ├── controllers/
│ │ ├── authController.py
│ │ ├── homeController.py
│ ├── static/
│ ├── css/
│ │ ├── style.css
│ ├── js/
│ ├── script.js
├── test/
│ ├── test_unitaire/
│
├── venv/ (Virtual environment - créez-le avec virtualenv ou venv)
│
├── config.py
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
```

## idée d'amélioration

- [ ] Ajouter un système de recherche
- [ ] Ajouter un système de suppression de compte
- [ ] Ajouter un système de suppression de message
- [ ] Ajouter un système de modification de message
- [ ] Ajouter un bot qui répond aux messages
