import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, sys, os, csv, uuid, Pmw

# === Fonctions JSON ===
def sauvegarder_taches():
    """Sauvegarde toutes les tâches dans un fichier JSON."""
    try:
        with open(FICHIER_TACHES, "w", encoding="utf-8") as f:
            # Enregistre une liste Python dans un fichier JSON
            json.dump(taches, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de sauvegarder : {e}")

def charger_taches():
    """Charge tasks.json dans la liste taches (créé s'il n'existe pas)."""
    global taches
    if os.path.exists(FICHIER_TACHES):                              # Vérifie si le fichier existe
            try:
                with open(FICHIER_TACHES, "r", encoding="utf-8") as f:
                    data = json.load(f)                                 # Lit le JSON pour recréer les données
                    for item in data:
                        if "id" not in item:
                            item["id"] = str(uuid.uuid4())
                    taches = data
            except Exception :
                # Si corrompu, on réinitialise
                taches = []
                with open(FICHIER_TACHES, "w", encoding="utf-8") as f:
                    json.dump([], f)
    else:
        taches = []
        with open(FICHIER_TACHES, "w", encoding="utf-8") as f:
            json.dump([], f)
    refresh_treeview()

# === Vue ===
def refresh_treeview():
    """Reconstruit la vue Treeview à partir de la liste 'taches'"""
    # vider l'affichage
    for it in tree.get_children():
        tree.delete(it)
    statut_var.set(value="Tous")

    for task in taches:
        titre = task.get("titre", "")
        statut = task.get("statut", "En attente")
        priorite = task.get("priorite", "Moyenne")
        iid = task.get("id")
        # assure un id
        if not iid:
            iid = str(uuid.uuid4())
            task["id"] = iid
        tree.insert("", tk.END, iid=iid, values=(titre, statut, priorite))
        colorer_ligne(iid, statut, priorite)

def filtrer_taches():
    """Reconstruit la vue Treeview à partir de la liste 'taches' en appliquant le filtre."""
    # vider l'affichage
    for it in tree.get_children():
        tree.delete(it)

    mot_cle = search_var.get().lower().strip()
    statut_filtre = statut_var.get()

    for task in taches:
        titre = task.get("titre", "")
        statut = task.get("statut", "En attente")
        priorite = task.get("priorite", "Moyenne")
        # filtration (mais sans modifier la liste taches)
        visible = True
        if mot_cle and mot_cle not in titre.lower():
            visible = False
        if statut_filtre != "Tous" and statut != statut_filtre:
            visible = False
        if visible:
            iid = task.get("id")
            # assure un id
            if not iid:
                iid = str(uuid.uuid4())
                task["id"] = iid
            tree.insert("", tk.END, iid=iid, values=(titre, statut, priorite))
            colorer_ligne(iid, statut, priorite)

def colorer_ligne(item, statut, priorite):
    if statut == "Faite":
        tree.item(item, tags=("done",))
    elif priorite == "Haute":
        tree.item(item, tags=("urgent",))
    else:
        tree.item(item, tags=("normal",))

# === Actions (opérations sur le modèle taches) ===
def ajouter_tache():
    titre = entry_titre.get().strip()
    priorite = priorite_var.get()
    if not titre:
        messagebox.showwarning("Champ vide", "Le titre de la tâche est obligatoire.")           # Fenêtres pop-up
        return
    # Ajouter la tâche au tableau
    nouvelle = {
        "id": str(uuid.uuid4()),
        "titre": titre,
        "statut": "En attente",
        "priorite": priorite
    }
    taches.append(nouvelle)
    sauvegarder_taches()                                                                        # Sauvegarde automatique
    refresh_treeview()
    # Réinitialiser les champs
    entry_titre.delete(0, tk.END)
    priorite_combobox.set("Moyenne")

def supprimer_tache():
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une tâche à supprimer.")
        return
    if not messagebox.askyesno("Confirmer", "Supprimer cette/ces tâche(s) ?"):
        return
    # supprimer dans la liste taches par id
    for iid in selection:
        taches[:] = [t for t in taches if t.get("id") != iid]
    sauvegarder_taches()
    refresh_treeview()

def marquer_faite():
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Aucune sélection", "Veuillez sélectionner une tâche à marquer comme faite.")
        return
    for iid in selection:
        for t in taches:
            if t.get("id") == iid:
                t["statut"] = "Faite"
                break
    sauvegarder_taches()
    refresh_treeview()

# === Export CSV ===
def exporter_csv():
    """Exporte les tâches dans un fichier CSV."""
    fichier = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Fichier CSV", "*.csv")],
        title="Exporter les tâches"
    )                                                  # Ouvre une boîte pour choisir le fichier CSV à créer
    if not fichier:
        return

    try:
        with open(fichier, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)                              # Permet d’écrire un tableau dans un fichier .csv
            writer.writerow(["Titre", "Statut", "Priorité"])    # en-têtes
            for t in taches:
                writer.writerow([t.get("titre",""), t.get("statut",""), t.get("priorite","")])
        messagebox.showinfo("Export réussi", f"Les tâches ont été exportées vers {fichier}.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'export : {e}")

# === Quitter proprement ===
def quitter_application():
    sauvegarder_taches()
    if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter TaskMaster ?"):
        root.destroy()


#-- PROGRAMME PRINCIPAL -- #
if getattr(sys, 'frozen', False):
    # Si l'app est compilée en exe
    base_path = sys._MEIPASS  # dossier temporaire PyInstaller
    data_path = os.path.join(os.path.dirname(sys.executable), 'tasks.json')
else:
    # En mode script
    base_path = os.path.dirname(__file__)
    data_path = os.path.join(base_path, 'tasks.json')

# Créer tasks.json s'il n'existe pas
if not os.path.exists(data_path):
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump([], f)

FICHIER_TACHES = data_path

# Création de la fenêtre principale
root = tk.Tk()                                                  # Crée la fenêtre principale
root.title("TaskMaster - Gestionnaire de tâches")               # Définit le nom affiché dans la barre de titre
root.geometry("650x580")                                        # Définit la taille (largeur x hauteur)
root.resizable(False, False)

# === Thème sombre (facultatif) ===
style = ttk.Style()
style.theme_use("clam")

root.configure(bg="#2E2E2E")
style.configure("Treeview",
                background="#3C3C3C",
                foreground="white",
                fieldbackground="#3C3C3C",
                font=("Segoe UI", 10))
style.configure("Treeview.Heading", background="#444", foreground="white", font=("Segoe UI", 10, "bold"))
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)
style.configure("TLabel", background="#2E2E2E", foreground="white", font=("Segoe UI", 10))
style.configure("TFrame", background="#2E2E2E")

# Gestion des bulles d'information
tip = Pmw.Balloon(root)

# === Modèle de données (source de vérité) ===
taches = []  # liste de dicts: {'id': str, 'titre': str, 'statut': str, 'priorite': str}

# Frame principale (zone de contenu)
main_frame = ttk.Frame(root, padding=10)                        # Conteneur pour organiser les widgets
main_frame.pack(fill="both", expand=True)

# Titre
title_label = ttk.Label(main_frame, text="📝 Mes tâches", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# === Zone de filtre / recherche ===
filter_frame = ttk.Frame(main_frame)
filter_frame.pack(fill="x", pady=5)

search_var = tk.StringVar()
search_entry = ttk.Entry(filter_frame, textvariable=search_var, width=30)
search_entry.pack(side="left", padx=5)
search_entry.insert(0, "Rechercher...")
tip.bind(search_entry, "Rechercher une tache...")

statut_var = tk.StringVar(value="Tous")
ttk.Label(filter_frame, text="Statut :").pack(side="left", padx=5)
statut_combobox = ttk.Combobox(filter_frame,
                               textvariable=statut_var,
                               values=["Tous", "En attente", "Faite"],
                               width=12, state="readonly")
statut_combobox.pack(side="left", padx=5)

btn_filtrer = ttk.Button(filter_frame, text="🔍 Filtrer", command=filtrer_taches)
btn_filtrer.pack(side="left", padx=5)

tip.bind(btn_filtrer, "Filtrer par mot clé et par statut")

# === Tableau (Treeview) ===
columns = ("Titre", "Statut", "Priorité")                   # Définition des colonnes

tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)    # tableau à plusieurs colonnes
tree.pack(fill="both", expand=True)

# Définir les titres des colonnes
tree.heading(columns[0], text=columns[0], anchor="w")                # définit le titre affiché de chaque colonne
tree.heading(columns[1], text=columns[1], anchor="e")
tree.heading(columns[2], text=columns[2], anchor="e")
tree.column(columns[0], width=360, anchor="w")                                  # confgure la taille et l'affichage des colonnes
tree.column(columns[1], width=70, anchor="e")
tree.column(columns[2], width=70, anchor="e")

# === Scrollbar ===
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Définition des tags (couleurs)
tree.tag_configure("done", background="#2F4F2F", foreground="#C0FFC0")
tree.tag_configure("urgent", background="#4B0000", foreground="#FFB6B6")
tree.tag_configure("normal", background="#3C3C3C", foreground="white")

# === Section formulaire d'ajout ===
form_frame = ttk.LabelFrame(main_frame, text="Ajouter une tâche", padding=10)           # Encadre visuellement la zone d’ajout
form_frame.pack(fill="x", pady=10)

# Champ titre
ttk.Label(form_frame, text="Titre :").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_titre = ttk.Entry(form_frame, width=25)
entry_titre.grid(row=0, column=1, padx=5, pady=5)
tip.bind(entry_titre, "Titre de la tache")

# Champ priorité
ttk.Label(form_frame, text="Priorité :").grid(row=0, column=2, padx=5, pady=5, sticky="w")
priorite_var = tk.StringVar()
priorite_combobox = ttk.Combobox(form_frame, textvariable=priorite_var, values=["Basse", "Moyenne", "Haute"], width=10, state="readonly")
priorite_combobox.grid(row=0, column=3, padx=5, pady=5)
tip.bind(priorite_combobox, "Niveau de priorite")
priorite_combobox.set("Moyenne")

btn_ajouter = ttk.Button(form_frame, text="Ajouter", command=ajouter_tache)
btn_ajouter.grid(row=0, column=4, padx=10)
tip.bind(btn_ajouter, "Créer une nouvelle tache")

# === Boutons d'action ===
action_frame = ttk.Frame(main_frame, padding=5)
action_frame.pack(fill="x")

btn_done = ttk.Button(action_frame, text="✔ Marquer comme faite", command=marquer_faite)
btn_done.pack(side="left", padx=5)
tip.bind(btn_done, "Marquer les taches sélectionnées comme faites")

btn_delete = ttk.Button(action_frame, text="🗑 Supprimer", command=supprimer_tache)
btn_delete.pack(side="left", padx=5)
tip.bind(btn_delete, "Supprimer les taches sélectionnées")

btn_export = ttk.Button(action_frame, text="📤 Exporter CSV", command=exporter_csv)
btn_export.pack(side="left", padx=5)
tip.bind(btn_export, "Exporter toutes les taches dans un fichier .CSV")

# === Charger les tâches existantes au démarrage ===
charger_taches()

# === Gestion de la fermeture ===
root.protocol("WM_DELETE_WINDOW", quitter_application)      # Intercepte la fermeture de la fenêtre pour sauvegarder avant de quitter

# Lancement de la boucle principale
root.mainloop()                                             # Lance le programme (boucle d’événements)