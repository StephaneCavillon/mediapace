# MediaPace Backend

API REST en Python/FastAPI pour gérer vos lectures et jeux vidéo.

## Tech Stack

- **Python 3.12**
- **FastAPI** - Framework web moderne
- **Peewee** - ORM pour SQLite
- **Pydantic** - Validation des données
- **SQLite** - Base de données

---

## Installation

### Prérequis

- Python 3.12+
- pip

### Setup environnement local

```bash
# 1. Créer un environnement virtuel
python3 -m venv venv

# 2. Activer l'environnement virtuel
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Installer les dépendances
pip install -r requirements.txt
```

---

## Développement

### Option 1 : En local (recommandé pour dev)

**Avantages :** Hot-reload rapide, debugging facile

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le serveur de développement
python src/main.py

# Ou avec uvicorn directement (plus d'options)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Accès :**
- API : http://localhost:8000
- Documentation interactive (Swagger) : http://localhost:8000/docs
- Documentation alternative (ReDoc) : http://localhost:8000/redoc

### Option 2 : Avec Docker

**Avantages :** Environnement isolé, identique à la production

```bash
# Depuis la racine du projet MediaPace
docker-compose up backend

# Ou avec rebuild (si requirements.txt a changé)
docker-compose up --build backend

# En arrière-plan
docker-compose up -d backend
```

---

## Structure du projet

```
Backend/
├── src/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration
│   ├── database.py          # Setup Peewee
│   ├── models/              # Modèles DB
│   │   ├── books.py
│   │   └── games.py
│   ├── schemas/             # Schémas Pydantic
│   │   ├── books.py
│   │   └── games.py
│   ├── routers/             # Routes API
│   │   ├── books.py
│   │   └── games.py
│   ├── services/            # Logique métier
│   │   ├── books_service.py
│   │   └── games_service.py
│   └── external/            # APIs externes
│       ├── google_books.py
│       └── howlongtobeat.py
├── data/                    # Base de données SQLite
│   └── db.sqlite
├── requirements.txt
├── Dockerfile
├── .env
└── README.md
```

---

## Configuration

### Variables d'environnement

Créer un fichier `.env` à la racine du dossier Backend :

```env
DATABASE_URL=sqlite:///data/db.sqlite
GOOGLE_BOOKS_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here
```

---

## Commandes utiles

### Développement local

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le serveur
python src/main.py

# Installer une nouvelle dépendance
pip install nom-du-package
pip freeze > requirements.txt  # Mettre à jour requirements.txt

# Désactiver l'environnement virtuel
deactivate
```

### Avec Docker

```bash
# Lancer tous les services (backend + frontend)
docker-compose up

# Lancer uniquement le backend
docker-compose up backend

# Rebuild après changement de requirements.txt
docker-compose up --build backend

# Arrêter les services
docker-compose down

# Voir les logs
docker-compose logs -f backend

# Accéder au shell du container
docker-compose exec backend bash

# Nettoyer les volumes (⚠️ supprime la DB)
docker-compose down -v
```

### Base de données

```bash
# Inspecter la DB avec sqlite3
sqlite3 data/db.sqlite

# Commandes SQLite utiles
.tables              # Lister les tables
.schema books        # Voir le schéma d'une table
SELECT * FROM books; # Query
.quit                # Quitter
```

---

## Tests API

### Avec curl

```bash
# Créer un livre
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "author": "George Orwell",
    "pages": 328
  }'

# Récupérer tous les livres
curl http://localhost:8000/api/books

# Récupérer un livre spécifique
curl http://localhost:8000/api/books/1

# Mettre à jour la progression
curl -X PATCH http://localhost:8000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"current_page": 50}'

# Supprimer un livre
curl -X DELETE http://localhost:8000/api/books/1
```

### Avec l'interface Swagger

Ouvrir http://localhost:8000/docs dans votre navigateur pour tester interactivement tous les endpoints.

---

## Debugging

### En local

```python
# Ajouter des logs
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")

# Ou des prints simples
print(f"Book: {book}")

# Debugger Python
import pdb; pdb.set_trace()
```

### Avec Docker

```bash
# Voir les logs en temps réel
docker-compose logs -f backend

# Accéder au container pour debug
docker-compose exec backend bash
python
>>> from src.models.books import Book
>>> books = Book.select()
>>> for book in books:
...     print(book.title)
```

---

## Workflow recommandé

### 1. Développement d'une nouvelle feature

```bash
# En local pour itérer rapidement
source venv/bin/activate
uvicorn src.main:app --reload
```

### 2. Test d'intégration Backend + Frontend

```bash
# Avec Docker
docker-compose up
```

### 3. Avant un commit

```bash
# Tester que tout fonctionne avec Docker
docker-compose up --build

# Vérifier les endpoints sur http://localhost:8000/docs
```

---

## Dépendances

Voir `requirements.txt` pour la liste complète. Principales dépendances :

- `fastapi[standard-no-fastapi-cloud-cli]` - Framework web
- `uvicorn` - Serveur ASGI
- `peewee` - ORM
- `pydantic-settings` - Configuration
- `httpx` - Client HTTP
- `howlongtobeatpy` - API HowLongToBeat

---

## Documentation

- **Guide de développement complet** : Voir `DEV_GUIDE.md`
- **FastAPI** : https://fastapi.tiangolo.com
- **Peewee** : http://docs.peewee-orm.com
- **Pydantic** : https://docs.pydantic.dev

---

## Troubleshooting

### Erreur : Module not found

```bash
# Vérifier que l'environnement virtuel est activé
which python  # Doit pointer vers venv/bin/python

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Erreur : Port 8000 déjà utilisé

```bash
# Trouver le processus
lsof -i :8000

# Tuer le processus
kill -9 <PID>

# Ou utiliser un autre port
uvicorn src.main:app --reload --port 8001
```

### Base de données corrompue

```bash
# Supprimer la DB et la recréer
rm data/db.sqlite
python src/main.py  # Recrée automatiquement les tables
```

### Hot-reload ne fonctionne pas avec Docker

```bash
# Vérifier les volumes dans docker-compose.yml
volumes:
  - ./Backend:/app  # Doit être présent

# Redémarrer les containers
docker-compose restart backend
```

---

## Contribution

1. Créer une branche pour votre feature
2. Développer en local avec hot-reload
3. Tester avec Docker
4. Commit et push

---

## License

Projet personnel MediaPace
