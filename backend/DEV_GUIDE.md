# Guide de développement MediaPace Backend

## Architecture FastAPI

```
Backend/
├── src/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py            # Configuration (env vars, settings)
│   ├── database.py          # Setup SQLite/Peewee
│   ├── models/              # Modèles DB (Peewee ORM)
│   │   ├── __init__.py
│   │   ├── books.py
│   │   └── games.py
│   ├── schemas/             # Validation API (Pydantic)
│   │   ├── __init__.py
│   │   ├── books.py
│   │   └── games.py
│   ├── routers/             # Routes/endpoints API
│   │   ├── __init__.py
│   │   ├── books.py
│   │   └── games.py
│   ├── services/            # Logique métier
│   │   ├── __init__.py
│   │   ├── books_service.py
│   │   └── games_service.py
│   └── external/            # APIs externes
│       ├── __init__.py
│       ├── google_books.py
│       └── howlongtobeat.py
├── data/                    # DB SQLite (gitignored)
├── requirements.txt
├── Dockerfile
└── .gitignore
```

## Ordre de développement

### Phase 1 : Configuration de base

#### 1.1 Dependencies (`requirements.txt`)
Ajouter les packages nécessaires :
- `peewee` - ORM pour gérer SQLite
- `pydantic-settings` - Gestion de la configuration
- `httpx` - Client HTTP pour APIs externes
- `howlongtobeatpy` - API HowLongToBeat
- `python-dotenv` - Variables d'environnement (optionnel)

#### 1.2 Configuration (`src/config.py`)
Créer une classe `Settings` avec `pydantic_settings.BaseSettings` :
- `database_url` : Chemin vers SQLite
- `google_books_api_key` : Clé API Google Books
- `openai_api_key` : Clé API OpenAI (futur)
- Charger depuis variables d'environnement

#### 1.3 Database (`src/database.py`)
Setup Peewee :
- Créer instance `db` avec `SqliteDatabase()`
- Créer classe `BaseModel` qui hérite de `peewee.Model`
- Configurer `BaseModel.Meta` avec la database
- Fonction `get_db()` pour gérer les connexions (optionnel avec Peewee)

**Concepts clés :**
- `SqliteDatabase` = connexion à la DB
- Peewee gère automatiquement les connexions
- `BaseModel` = classe parente pour tous les modèles
- Pas besoin de sessions explicites comme SQLAlchemy

---

### Phase 2 : Modèles de données (Peewee)

#### 2.1 Books Model (`src/models/books.py`)
Créer classe `Book(BaseModel)` avec champs :
- `id` : AutoField (primary_key automatique)
- `google_books_id` : CharField, unique=True, null=True
- `title` : CharField, null=False
- `author` : CharField, null=True
- `pages` : IntegerField, null=True
- `current_page` : IntegerField, default=0
- `status` : CharField, default="to_read"
- `cover_url` : CharField, null=True
- `created_at` : DateTimeField, default=datetime.now
- `updated_at` : DateTimeField, default=datetime.now

#### 2.2 Games Model (`src/models/games.py`)
Créer classe `Game(BaseModel)` avec champs :
- `id` : AutoField (primary_key automatique)
- `title` : CharField, null=False
- `platform` : CharField, null=True
- `completion_time` : FloatField, null=True
- `hours_played` : FloatField, default=0
- `status` : CharField, default="to_play"
- `cover_url` : CharField, null=True
- `created_at` : DateTimeField, default=datetime.now
- `updated_at` : DateTimeField, default=datetime.now

**Concepts clés :**
- Les champs Peewee définissent automatiquement les colonnes
- Pas besoin de `__tablename__`, Peewee le génère automatiquement
- Hériter de `BaseModel` pour que Peewee reconnaisse le modèle
- `AutoField` crée automatiquement un ID auto-incrémenté

---

### Phase 3 : Schémas Pydantic (Validation)

#### 3.1 Books Schemas (`src/schemas/books.py`)
Créer 3 classes Pydantic :

**BookBase** : Champs communs
- title, author, pages, google_books_id

**BookCreate(BookBase)** : Pour créer un livre
- Hérite de BookBase

**BookUpdate(BaseModel)** : Pour modifier un livre
- current_page (Optional)
- status (Optional)

**BookResponse(BookBase)** : Pour retourner un livre
- id, current_page, status, cover_url, created_at
- `Config: from_attributes = True` pour compatibilité Peewee

#### 3.2 Games Schemas (`src/schemas/games.py`)
Même logique que books :
- `GameBase`, `GameCreate`, `GameUpdate`, `GameResponse`

**Concepts clés :**
- Pydantic valide automatiquement les données
- `Optional[type]` = champ non requis
- `from_attributes = True` permet de convertir modèle Peewee → Pydantic

---

### Phase 4 : API FastAPI

#### 4.1 Main App (`src/main.py`)
Créer l'application FastAPI :
1. Importer FastAPI
2. Créer instance `app = FastAPI(title="MediaPace API")`
3. Créer les tables : `db.create_tables([Book, Game])`
4. Inclure les routers : `app.include_router(books.router, prefix="/api/books")`
5. Route root : `@app.get("/")` qui retourne un message de bienvenue
6. Point d'entrée : `if __name__ == "__main__": uvicorn.run(app, host="0.0.0.0", port=8000)`
   - Ce bloc permet de lancer l'API directement avec `python src/main.py`
   - `host="0.0.0.0"` expose l'API sur toutes les interfaces réseau (nécessaire pour Docker)
   - `port=8000` définit le port d'écoute
   - En production Docker, uvicorn est généralement lancé via la commande dans le Dockerfile

**Concepts clés :**
- Pas besoin de CORS en Docker : les services communiquent via le réseau Docker interne
- `prefix` ajoute un préfixe à toutes les routes du router
- `tags` organise la documentation Swagger

#### 4.2 Books Router (`src/routers/books.py`)
Créer `router = APIRouter()` avec endpoints :

**GET /api/books** : Liste tous les livres
- Response: `List[BookResponse]`
- Pas besoin de `Depends(get_db)` avec Peewee (connexion automatique)

**POST /api/books** : Créer un livre
- Body: `BookCreate`
- Response: `BookResponse`

**GET /api/books/{book_id}** : Récupérer un livre
- Path param: `book_id: int`
- Response: `BookResponse`
- Raise `HTTPException(404)` si non trouvé

**PATCH /api/books/{book_id}** : Modifier un livre
- Path param: `book_id: int`
- Body: `BookUpdate`
- Response: `BookResponse`

**DELETE /api/books/{book_id}** : Supprimer un livre
- Path param: `book_id: int`
- Response: `{"message": "Book deleted"}`

#### 4.3 Games Router (`src/routers/games.py`)
Même structure que books router

**Concepts clés :**
- `@router.get()`, `@router.post()` définissent les routes
- Peewee gère automatiquement les connexions (pas besoin de dependency injection)
- `response_model` valide et sérialise la réponse

---

### Phase 5 : Services (Logique métier)

#### 5.1 Books Service (`src/services/books_service.py`)
Créer classe `BooksService` :

**`__init__(self)`** : Pas besoin de stocker la DB avec Peewee

**`get_all_books()`** : Retourne tous les livres
- `Book.select()`

**`get_book(book_id: int)`** : Retourne un livre
- `Book.get_by_id(book_id)` ou `Book.get(Book.id == book_id)`

**`create_book(book: BookCreate)`** : Crée un livre
- `Book.create(**book.model_dump())`
- Retourne automatiquement l'instance créée

**`update_book(book_id: int, book_update: BookUpdate)`** : Modifie un livre
- Récupérer le livre avec `Book.get_by_id(book_id)`
- Mettre à jour : `book.update(**book_update.model_dump(exclude_unset=True)).where(Book.id == book_id).execute()`
- Ou modifier l'instance puis `book.save()`

**`delete_book(book_id: int)`** : Supprime un livre
- `Book.delete_by_id(book_id)` ou récupérer puis `book.delete_instance()`

#### 5.2 Games Service (`src/services/games_service.py`)
Même structure que books service

**Concepts clés :**
- Services séparent la logique métier des routes
- `model_dump()` convertit Pydantic en dict
- `exclude_unset=True` ignore les champs non fournis dans l'update
- Peewee commit automatiquement (pas besoin de `commit()` explicite)
- `create()` et `save()` persistent automatiquement

---

### Phase 6 : APIs externes

#### 6.1 Google Books API (`src/external/google_books.py`)
Créer fonction `search_books(query: str, api_key: str)` :
- Utiliser `httpx.get()` pour appeler l'API
- URL : `https://www.googleapis.com/books/v1/volumes?q={query}`
- Parser la réponse JSON
- Retourner liste de livres formatés

#### 6.2 HowLongToBeat (`src/external/howlongtobeat.py`)
Créer fonction `search_game(title: str)` :
- Utiliser la lib `howlongtobeatpy`
- Retourner infos du jeu (temps de complétion, etc.)

**Concepts clés :**
- `httpx` est async-compatible (meilleur que `requests`)
- Toujours gérer les erreurs API (try/except)
- Parser et valider les données externes

---

## Concepts Python/FastAPI à maîtriser

### Database Connection (Peewee)
```python
# Peewee gère automatiquement les connexions
# Pas besoin de dependency injection comme SQLAlchemy

@router.get("/books")
def get_books():
  books = Book.select()
  return list(books)

# Si besoin de gérer manuellement :
from src.database import db

@app.on_event("startup")
def startup():
  db.connect()

@app.on_event("shutdown")
def shutdown():
  db.close()
```

### Type Hints
```python
def create_book(book: BookCreate) -> BookResponse:
  # Python valide les types automatiquement
```

### Pydantic Models
```python
class BookCreate(BaseModel):
  title: str
  pages: Optional[int] = None

book = BookCreate(title="Test")  # Validation auto
```

### Peewee ORM
```python
# Query
books = Book.select().where(Book.status == "reading")

# Create
book = Book.create(title="Test", author="Author")
# Ou
book = Book(title="Test", author="Author")
book.save()

# Update
book = Book.get_by_id(1)
book.current_page = 50
book.save()
# Ou
Book.update(current_page=50).where(Book.id == 1).execute()

# Delete
book.delete_instance()
# Ou
Book.delete_by_id(1)
```

---

## Commandes utiles

### Lancer l'API
```bash
docker-compose up --build
```

### Tester l'API
```bash
# Documentation interactive
http://localhost:8000/docs

# Tester un endpoint
curl http://localhost:8000/api/books

# Créer un livre
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book", "author": "Author"}'
```

### Debug
```bash
# Logs du container
docker-compose logs -f backend

# Shell dans le container
docker-compose exec backend bash

# Inspecter la DB
sqlite3 data/app.db
```

### Tests et couverture de code
```bash
# Lancer tous les tests
pytest tests/

# Lancer les tests avec couverture
pytest --cov=src tests/

# Rapport détaillé avec lignes manquantes
pytest --cov=src --cov-report=term-missing tests/

# Générer un rapport HTML interactif
pytest --cov=src --cov-report=html tests/
# Ouvrir htmlcov/index.html dans le navigateur

# Lancer un fichier de test spécifique
pytest tests/test_service_book.py

# Lancer un test spécifique
pytest tests/test_service_book.py::test_book_creation

# Mode verbose pour plus de détails
pytest -v tests/

# Afficher les print() dans les tests
pytest -s tests/
```

---

## Ressources

- **FastAPI** : https://fastapi.tiangolo.com
- **Peewee** : http://docs.peewee-orm.com
- **Pydantic** : https://docs.pydantic.dev
- **Google Books API** : https://developers.google.com/books

---

## Checklist de progression

- [x] Phase 1 : Configuration (config.py, database.py)
- [x] Phase 2 : Modèles (books.py, games.py)
- [x] Phase 3 : Schémas (schemas/books.py, schemas/games.py)
- [x] Phase 4 : API (main.py, routers)
- [x] Phase 5 : Services (books_service.py, games_service.py)
- [ ] Phase 6 : APIs externes (google_books.py, howlongtobeat.py)
- [ ] Tests : Tester tous les endpoints avec curl ou Swagger
- [ ] Frontend : Connecter React à l'API

---

## Notes importantes

1. **Toujours créer les `__init__.py`** dans chaque dossier Python
2. **Utiliser 2 espaces** pour l'indentation (selon vos préférences)
3. **Pas de point-virgule** à la fin des lignes
4. **Tester chaque phase** avant de passer à la suivante
5. **Consulter la doc** quand vous bloquez sur un concept
