# Projet Python avec Flask et SQLite

Ce projet est un exemple d'application Python utilisant le framework Flask pour créer un serveur web et SQLite comme base de données.

## Installation

1. Clonez ce dépôt sur votre machine locale :


2. Installez les dépendances du projet :

    ```bash
    pip install -r requirements.txt
    ```
   
3. Lancez le serveur de développement :

    ```bash
    python run.py
    ```
   
4. Ouvrez votre navigateur à l'adresse [http://localhost:5000](http://localhost:5000).

## Utilisation

Capture d'écran

## structure du projet

```md
python_chat/
│
├── app/
│   ├── __init__.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── private_message.html
│   ├── model/
│   │   ├── user_model.py
│   │   ├── message_model.py
│   ├── controllers/
│   │   ├── authController.py
│   │   ├── homeController.py
│   ├── static/
│       ├── css/
│       │   ├── style.css
│       ├── js/
│           ├── script.js
├── test/
│   ├── test_unitaire/
│
├── venv/  (Virtual environment - créez-le avec virtualenv ou venv)
│
├── config.py
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
```
