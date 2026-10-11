# EasySchool Cameroun

Plateforme d'apprentissage en ligne pour le secondaire camerounais : cours, exercices, quiz, forums,
assistant IA, anciennes épreuves, et **dépôt d'épreuves par les élèves** (25 FCFA par épreuve nouvelle).

- Rapport d'audit et correctifs : [SECURITE.md](SECURITE.md)
- Python 3.12+, Django 5.2 LTS

## Lancer en local (5 minutes)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "DEBUG=True" > .env
echo "ACCOUNT_EMAIL_VERIFICATION=optional" >> .env
python manage.py migrate
DEMO_ADMIN_EMAIL=admin@demo.cm DEMO_ADMIN_PASSWORD=ChangeMoi-2026 \
DEMO_ELEVE_EMAIL=eleve@demo.cm DEMO_ELEVE_PASSWORD=ChangeMoi-2026 python manage.py init_demo
python manage.py runserver
```

Sans Redis, les tâches Celery s'exécutent directement ; sans clé Brevo, les e-mails s'affichent dans le terminal.

## Mettre en ligne gratuitement sur Render

1. Pousse ce dossier sur un dépôt GitHub (privé de préférence).
2. Sur [render.com](https://render.com) : **New > Blueprint**, choisis le dépôt. Render lit `render.yaml`
   et crée la base PostgreSQL gratuite + le site.
3. Renseigne quand Render les demande : `DEMO_ADMIN_EMAIL`, `DEMO_ADMIN_PASSWORD`, `DEMO_ELEVE_EMAIL`,
   `DEMO_ELEVE_PASSWORD` (et plus tard `BREVO_API_KEY`, `GEMINI_API_KEY`…).
4. Le site est disponible sur `https://easyschool-xxxx.onrender.com`. L'adresse de l'administration
   Django est la valeur de la variable `ADMIN_URL` (générée au hasard, visible dans Render > Environment).

Limites de l'offre gratuite de Render : le site s'endort après 15 minutes sans visite (≈ 1 min pour se réveiller),
la base PostgreSQL gratuite expire au bout de 30 jours, et les fichiers envoyés sont effacés à chaque redéploiement.
Pour la production, renseigne `AWS_STORAGE_BUCKET_NAME` (les épreuves vont alors dans un dossier S3 privé)
ou utilise ton serveur avec `docker-compose.yml` + `nginx/easyschool.conf`.

## Module « Dépôt d'épreuves » (`depot/`)

- Adresse : `/depot/` (liens dans le menu du site, la page d'accueil et l'espace élève).
- Formats : PDF, JPG, PNG, WEBP — 10 Mo max, 40 pages max, 20 envois par élève et par jour.
- **Une épreuve ne peut être envoyée qu'une fois.** L'envoi est refusé si :
  1. le fichier est identique à un fichier déjà reçu (empreinte SHA-256) ;
  2. le texte du PDF, normalisé, est identique (fichier renommé ou ré-enregistré) ;
  3. l'image ou la page scannée est visuellement identique (recompressée, redimensionnée) ;
  4. une épreuve du même établissement, de la même classe, matière, évaluation et année existe déjà.
  Les contraintes `UNIQUE` de la base empêchent aussi deux envois simultanés.
- Si l'épreuve est acceptée : enregistrement en base, fichier stocké hors des médias publics,
  **+25 FCFA** sur le solde (`somme`) et une ligne dans le journal `MouvementSolde`, le tout dans une seule transaction.
- Administration : *Épreuves soumises* > actions **Valider** ou **Rejeter** (le rejet reprend les 25 F).
- Réglages : `DEPOT_RECOMPENSE_FCFA`, `DEPOT_TAILLE_MAX_MO`, `DEPOT_LIMITE_PAR_JOUR`.

## Tests

```bash
python manage.py test
```
