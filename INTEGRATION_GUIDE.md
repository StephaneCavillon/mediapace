# Guide d'intégration MediaPace - Backend ↔ Frontend

## Vue d'ensemble

Ce guide explique comment connecter le backend Python/FastAPI avec le frontend React, gérer les variables d'environnement, et déployer l'application complète.

---

## Architecture complète

```
MediaPace/
├── Backend/
│   ├── src/
│   ├── data/              # DB SQLite (gitignored)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env              # Variables d'environnement backend
├── Frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── .env              # Variables d'environnement frontend
├── docker-compose.yml     # Orchestration des services
├── .gitignore
└── README.md
```

---

## Phase 1 : Variables d'environnement

### Backend `.env` (`Backend/.env`)

```env
# Database
DATABASE_URL=sqlite:///app/data/app.db

# APIs externes
GOOGLE_BOOKS_API_KEY=your_google_books_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# CORS (optionnel)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend `.env` (`Frontend/.env`)

```env
# API Backend
VITE_API_URL=http://localhost:8000/api

# Mode
VITE_MODE=development
```

**⚠️ Important :**
- Variables Vite doivent commencer par `VITE_`
- Ne jamais commit les `.env` avec des vraies clés API
- Ajouter `.env` dans `.gitignore`

---

## Phase 2 : Configuration Docker

### Backend Dockerfile (`Backend/Dockerfile`)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "src/main.py"]
```

### Frontend Dockerfile (`Frontend/Dockerfile`)

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host"]
```

### docker-compose.yml (racine du projet)

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./Backend
      dockerfile: Dockerfile
    container_name: mediapace-backend
    ports:
      - "8000:8000"
    volumes:
      - ./Backend:/app
    environment:
      - DATABASE_URL=sqlite:///app/data/app.db
      - GOOGLE_BOOKS_API_KEY=${GOOGLE_BOOKS_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    networks:
      - mediapace-network
    restart: unless-stopped

  frontend:
    build:
      context: ./Frontend
      dockerfile: Dockerfile
    container_name: mediapace-frontend
    ports:
      - "3000:3000"
    volumes:
      - ./Frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000/api
    depends_on:
      - backend
    networks:
      - mediapace-network
    restart: unless-stopped

networks:
  mediapace-network:
    driver: bridge
```

**Concepts clés :**
- `networks` permet la communication entre containers
- `depends_on` assure que le backend démarre avant le frontend
- `volumes` permettent le hot-reload en dev
- `/app/node_modules` évite de partager node_modules avec l'host

---

## Phase 3 : Communication Backend ↔ Frontend

### 3.1 Configuration CORS (Backend)

Dans `Backend/src/main.py` :

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "http://localhost:3000",
    "http://localhost:5173",  # Vite dev server
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
```

**⚠️ Production :**
- Remplacer `["*"]` par les origines spécifiques
- Ne jamais utiliser `allow_origins=["*"]` avec `allow_credentials=True`

### 3.2 Client API (Frontend)

Dans `Frontend/src/services/api.js` :

```js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Intercepteur pour les erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export default api
```

### 3.3 Exemple d'appel API (Frontend)

Dans `Frontend/src/services/booksApi.js` :

```js
import api from './api'

export const booksApi = {
  getAll: () => api.get('/books'),
  getById: (id) => api.get(`/books/${id}`),
  create: (data) => api.post('/books', data),
  update: (id, data) => api.patch(`/books/${id}`, data),
  delete: (id) => api.delete(`/books/${id}`),
}
```

Dans un composant React :

```jsx
import { useEffect, useState } from 'react'
import { booksApi } from '@/services/booksApi'

function BooksList() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await booksApi.getAll()
        setBooks(response.data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchBooks()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      {books.map(book => (
        <div key={book.id}>{book.title}</div>
      ))}
    </div>
  )
}
```

---

## Phase 4 : Gestion des erreurs

### Backend - Erreurs HTTP

Dans `Backend/src/routers/books.py` :

```python
from fastapi import HTTPException

@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
  book = service.get_book(book_id)
  if not book:
    raise HTTPException(status_code=404, detail="Book not found")
  return book
```

### Frontend - Gestion des erreurs

```jsx
const handleAddBook = async (bookData) => {
  try {
    const response = await booksApi.create(bookData)
    setBooks([...books, response.data])
    toast.success('Book added successfully!')
  } catch (error) {
    if (error.response?.status === 400) {
      toast.error('Invalid book data')
    } else if (error.response?.status === 500) {
      toast.error('Server error, please try again')
    } else {
      toast.error('An error occurred')
    }
  }
}
```

**Installer react-hot-toast :**
```bash
npm install react-hot-toast
```

---

## Phase 5 : Déploiement

### Développement local

```bash
# Démarrer tous les services
docker-compose up --build

# Arrêter les services
docker-compose down

# Voir les logs
docker-compose logs -f

# Rebuild un service spécifique
docker-compose up --build backend
```

### Production (exemple avec Docker)

**docker-compose.prod.yml :**

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./Backend
      dockerfile: Dockerfile.prod
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///app/data/app.db
      - GOOGLE_BOOKS_API_KEY=${GOOGLE_BOOKS_API_KEY}
    volumes:
      - backend-data:/app/data
    restart: always

  frontend:
    build:
      context: ./Frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always

volumes:
  backend-data:
```

**Backend/Dockerfile.prod :**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend/Dockerfile.prod :**

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Frontend/nginx.conf :**

```nginx
server {
  listen 80;
  server_name localhost;

  root /usr/share/nginx/html;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }

  location /api {
    proxy_pass http://backend:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
  }
}
```

---

## Phase 6 : Tests d'intégration

### Test manuel avec curl

```bash
# Créer un livre
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book", "author": "Test Author", "pages": 300}'

# Récupérer tous les livres
curl http://localhost:8000/api/books

# Mettre à jour un livre
curl -X PATCH http://localhost:8000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"current_page": 50}'

# Supprimer un livre
curl -X DELETE http://localhost:8000/api/books/1
```

### Test avec Postman/Insomnia

1. Importer les endpoints depuis http://localhost:8000/docs
2. Tester chaque endpoint
3. Vérifier les réponses et codes HTTP

### Tests automatisés (optionnel)

**Backend - pytest :**

```bash
pip install pytest pytest-asyncio httpx
```

```python
# Backend/tests/test_books.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_book():
  response = client.post("/api/books", json={
    "title": "Test Book",
    "author": "Test Author",
    "pages": 300
  })
  assert response.status_code == 200
  assert response.json()["title"] == "Test Book"
```

**Frontend - Vitest :**

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

```jsx
// Frontend/src/components/BookCard.test.jsx
import { render, screen } from '@testing-library/react'
import { BookCard } from './BookCard'

test('renders book title', () => {
  render(<BookCard title="Test Book" author="Test Author" />)
  expect(screen.getByText('Test Book')).toBeInTheDocument()
})
```

---

## Phase 7 : Debugging

### Backend

**Logs Python :**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

**Accéder au container :**
```bash
docker-compose exec backend bash
python
>>> from src.database import SessionLocal
>>> db = SessionLocal()
>>> from src.models.books import Book
>>> books = db.query(Book).all()
>>> print(books)
```

### Frontend

**Console logs :**
```jsx
console.log('Books:', books)
console.error('Error:', error)
console.table(books)
```

**React DevTools :**
- Installer l'extension Chrome/Firefox
- Inspecter les composants et leur state

**Network tab :**
- Vérifier les requêtes API
- Voir les payloads et réponses
- Vérifier les headers CORS

---

## Phase 8 : Optimisations

### Backend

**Caching avec Redis (futur) :**
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
  redis = aioredis.from_url("redis://localhost")
  FastAPICache.init(RedisBackend(redis), prefix="mediapace:")
```

**Pagination :**
```python
@router.get("/")
def get_books(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
  books = db.query(Book).offset(skip).limit(limit).all()
  return books
```

### Frontend

**Lazy loading :**
```jsx
import { lazy, Suspense } from 'react'

const BooksPage = lazy(() => import('./pages/Books'))

<Suspense fallback={<Loading />}>
  <BooksPage />
</Suspense>
```

**Memoization :**
```jsx
import { useMemo } from 'react'

const filteredBooks = useMemo(() => {
  return books.filter(book => book.status === 'reading')
}, [books])
```

**React Query (recommandé) :**
```bash
npm install @tanstack/react-query
```

```jsx
import { useQuery } from '@tanstack/react-query'

const { data: books, isLoading, error } = useQuery({
  queryKey: ['books'],
  queryFn: () => booksApi.getAll().then(res => res.data)
})
```

---

## Checklist complète

### Setup
- [ ] Variables d'environnement configurées
- [ ] Docker Compose fonctionnel
- [ ] CORS configuré
- [ ] Client API configuré

### Backend
- [ ] API endpoints créés
- [ ] Base de données initialisée
- [ ] Validation des données
- [ ] Gestion des erreurs

### Frontend
- [ ] Pages créées
- [ ] Composants créés
- [ ] Appels API fonctionnels
- [ ] Gestion des états (loading, error)

### Intégration
- [ ] Communication Backend ↔ Frontend
- [ ] Tests manuels réussis
- [ ] Gestion des erreurs end-to-end
- [ ] Documentation API (Swagger)

### Production
- [ ] Dockerfiles de production
- [ ] Variables d'environnement sécurisées
- [ ] Tests automatisés
- [ ] Monitoring et logs

---

## Commandes essentielles

```bash
# Développement
docker-compose up --build
docker-compose down
docker-compose logs -f

# Production
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml down

# Debug
docker-compose exec backend bash
docker-compose exec frontend sh

# Nettoyage
docker-compose down -v  # Supprime les volumes
docker system prune -a  # Nettoie tout Docker
```

---

## Ressources

- **FastAPI CORS** : https://fastapi.tiangolo.com/tutorial/cors/
- **Axios** : https://axios-http.com
- **Docker Compose** : https://docs.docker.com/compose/
- **React Query** : https://tanstack.com/query/latest
- **Nginx** : https://nginx.org/en/docs/

---

## Troubleshooting

### Problème : CORS error
**Solution :** Vérifier que le backend autorise l'origine du frontend dans `allow_origins`

### Problème : Connection refused
**Solution :** Vérifier que les containers sont sur le même réseau Docker

### Problème : 404 sur les routes React
**Solution :** Configurer nginx pour rediriger vers index.html (SPA)

### Problème : Hot reload ne fonctionne pas
**Solution :** Vérifier les volumes dans docker-compose.yml

### Problème : Variables d'environnement non chargées
**Solution :** Redémarrer les containers après modification des .env
