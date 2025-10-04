📝 TaskMaster

TaskMaster est une application de gestion de tâches simple et élégante, développée en Python (Tkinter).
Elle permet d’ajouter, modifier, filtrer et sauvegarder automatiquement vos tâches dans un fichier JSON.

🚀 Fonctionnalités principales

✅ Ajouter une tâche avec titre et priorité
✅ Supprimer ou marquer une tâche comme "faite"
✅ Sauvegarde automatique dans un fichier tasks.json
✅ Recherche par mot-clé et filtrage par statut
✅ Export des tâches au format CSV
✅ Interface graphique moderne (Tkinter)

📦 Installation
1️⃣ Cloner le dépôt
git clone https://github.com/borismessobo2015-maker/TaskMaster.git
cd TaskMaster

2️⃣ Installer Python

Télécharge Python depuis python.org/downloads

Version recommandée : Python 3.8 ou supérieur

3️⃣ Installer les dépendances

(Tkinter est inclus dans Python, donc rien à installer de spécial)

pip install -r requirements.txt

4️⃣ Lancer l’application
python main.py

🧰 Fichier de sauvegarde

Les tâches sont automatiquement enregistrées dans :

tasks.json


Si le fichier n’existe pas, il sera créé automatiquement au premier lancement.

⚙️ Créer un exécutable (.exe)

Tu peux générer un exécutable Windows avec PyInstaller
.

Installation
pip install pyinstaller

Compilation
pyinstaller --onefile --windowed main.py


L’exécutable sera créé dans :

dist/main.exe

Inclure le fichier JSON (optionnel)

Si tu veux que tasks.json soit intégré directement dans le .exe :

pyinstaller --onefile --windowed --add-data "tasks.json;." main.py

📤 Export CSV

L’application permet d’exporter la liste complète des tâches dans un fichier .csv
afin de les sauvegarder ou de les consulter avec Excel.

🧩 Structure du projet
TaskMaster/
│
├── main.py           # Script principal
├── tasks.json        # Fichier de données (auto-créé)
├── README.md         # Description du projet
├── .gitignore        # Fichiers à ignorer dans Git
└── requirements.txt  # Dépendances du projet

🧑‍💻 Auteur

Projet réalisé par Boris MESSOBO
📧 Contact : borismessobo2015@gmail.com

💼 GitHub : github.com/borismessobo2015-maker

🪪 Licence

Ce projet est sous licence MIT — vous êtes libre de le réutiliser, le modifier et le partager.

MIT License © 2025 Boris MESSOBO

🌍 English Version

TaskMaster is a simple and elegant Python (Tkinter) task manager.
It allows you to add, edit, filter, and automatically save your tasks to a JSON file.

Features

Add, delete, and mark tasks as "done"

Auto-save to tasks.json

Search and filter by status

Export tasks to CSV

Clean Tkinter GUI

Run
python main.py

Build Executable
pyinstaller --onefile --windowed main.py


⭐ If you like this project, give it a star on GitHub!