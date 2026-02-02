# Guide de développement MediaPace Frontend

## Architecture React + Vite

```
Frontend/
├── public/
│   └── assets/           # Images, icônes statiques
├── src/
│   ├── main.jsx          # Point d'entrée React
│   ├── App.jsx           # Composant racine
│   ├── components/       # Composants réutilisables
│   │   ├── ui/          # shadcn/ui components
│   │   ├── layout/      # Header, Footer, Sidebar
│   │   ├── books/       # Composants livres
│   │   └── games/       # Composants jeux
│   ├── pages/           # Pages de l'application
│   │   ├── Home.jsx
│   │   ├── Books.jsx
│   │   ├── Games.jsx
│   │   └── Stats.jsx
│   ├── services/        # Appels API
│   │   ├── api.js       # Client HTTP configuré
│   │   ├── booksApi.js
│   │   └── gamesApi.js
│   ├── hooks/           # Custom React hooks
│   │   ├── useBooks.js
│   │   └── useGames.js
│   ├── store/           # State management (optionnel)
│   │   └── store.js
│   ├── utils/           # Fonctions utilitaires
│   │   └── helpers.js
│   └── styles/          # CSS global
│       └── index.css
├── index.html
├── vite.config.js
├── tailwind.config.js
├── package.json
└── Dockerfile
```

## Ordre de développement

### Phase 1 : Setup initial

#### 1.1 Initialiser le projet Vite
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

#### 1.2 Installer les dépendances
```bash
# TailwindCSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# shadcn/ui
npx shadcn-ui@latest init

# Routing
npm install react-router-dom

# HTTP Client
npm install axios

# Icons
npm install lucide-react

# Forms (optionnel)
npm install react-hook-form zod @hookform/resolvers
```

#### 1.3 Configurer TailwindCSS (`tailwind.config.js`)
```js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

#### 1.4 Configurer Vite (`vite.config.js`)
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
  },
})
```

---

### Phase 2 : Configuration API

#### 2.1 Client API (`src/services/api.js`)
Créer une instance axios configurée :
- Base URL : `http://localhost:8000/api`
- Headers par défaut
- Intercepteurs pour gérer les erreurs
- Timeout

**Concepts clés :**
- Centraliser la config API
- Gérer les erreurs globalement
- Ajouter des intercepteurs pour les tokens (futur auth)

#### 2.2 Books API (`src/services/booksApi.js`)
Créer les fonctions d'appel API :
- `getBooks()` : GET /books
- `getBook(id)` : GET /books/:id
- `createBook(data)` : POST /books
- `updateBook(id, data)` : PATCH /books/:id
- `deleteBook(id)` : DELETE /books/:id

#### 2.3 Games API (`src/services/gamesApi.js`)
Même structure que booksApi

**Concepts clés :**
- Chaque fonction retourne une Promise
- Utiliser async/await
- Gérer les erreurs avec try/catch

---

### Phase 3 : Routing

#### 3.1 Setup Router (`src/App.jsx`)
Configurer React Router :
- Route `/` : Page d'accueil
- Route `/books` : Liste des livres
- Route `/books/:id` : Détail d'un livre
- Route `/games` : Liste des jeux
- Route `/games/:id` : Détail d'un jeu
- Route `/stats` : Statistiques

**Concepts clés :**
- `BrowserRouter` englobe toute l'app
- `Routes` et `Route` définissent les chemins
- `useNavigate()` pour la navigation programmatique
- `useParams()` pour récupérer les paramètres d'URL

---

### Phase 4 : Layout

#### 4.1 Header (`src/components/layout/Header.jsx`)
Créer la barre de navigation :
- Logo MediaPace
- Liens : Books, Games, Stats
- Bouton de recherche (futur)

#### 4.2 Sidebar (`src/components/layout/Sidebar.jsx`)
Menu latéral (optionnel) :
- Navigation principale
- Filtres rapides
- Statistiques résumées

#### 4.3 Layout principal (`src/components/layout/Layout.jsx`)
Wrapper qui contient Header + contenu + Footer

**Concepts clés :**
- `children` prop pour injecter le contenu
- Composants réutilisables
- Responsive design avec TailwindCSS

---

### Phase 5 : Pages principales

#### 5.1 Home Page (`src/pages/Home.jsx`)
Page d'accueil :
- Vue d'ensemble (livres en cours, jeux en cours)
- Statistiques rapides
- Dernières activités
- Call-to-action pour ajouter du contenu

#### 5.2 Books Page (`src/pages/Books.jsx`)
Liste des livres :
- Grille de cartes de livres
- Filtres (status : to_read, reading, finished)
- Bouton "Ajouter un livre"
- Barre de recherche

#### 5.3 Book Detail Page (`src/pages/BookDetail.jsx`)
Détail d'un livre :
- Couverture, titre, auteur
- Progression (current_page / total_pages)
- Barre de progression visuelle
- Boutons : Modifier, Supprimer
- Formulaire de mise à jour de la page actuelle

#### 5.4 Games Page (`src/pages/Games.jsx`)
Liste des jeux (même structure que Books)

#### 5.5 Stats Page (`src/pages/Stats.jsx`)
Statistiques :
- Nombre de livres lus cette année
- Nombre de pages lues
- Temps de jeu total
- Graphiques (optionnel, utiliser recharts ou chart.js)

**Concepts clés :**
- `useState()` pour l'état local
- `useEffect()` pour charger les données
- Conditional rendering avec `{condition && <Component />}`
- Loading states et error handling

---

### Phase 6 : Composants Books

#### 6.1 BookCard (`src/components/books/BookCard.jsx`)
Carte d'un livre :
- Couverture (image)
- Titre et auteur
- Progression (%)
- Badge de status
- Click pour aller au détail

#### 6.2 BookForm (`src/components/books/BookForm.jsx`)
Formulaire d'ajout/modification :
- Champs : titre, auteur, pages
- Recherche Google Books (bouton)
- Validation avec react-hook-form + zod
- Submit vers l'API

#### 6.3 BookProgress (`src/components/books/BookProgress.jsx`)
Barre de progression :
- Visuel de la progression
- Input pour mettre à jour la page actuelle
- Calcul automatique du pourcentage

#### 6.4 BookSearch (`src/components/books/BookSearch.jsx`)
Recherche de livres :
- Input de recherche
- Appel à Google Books API via le backend
- Liste de résultats
- Bouton "Ajouter" pour chaque résultat

**Concepts clés :**
- Props pour passer les données
- Callbacks pour remonter les événements
- Composants contrôlés vs non contrôlés
- Debouncing pour la recherche

---

### Phase 7 : Composants Games

#### 7.1 GameCard (`src/components/games/GameCard.jsx`)
Carte d'un jeu (similaire à BookCard)

#### 7.2 GameForm (`src/components/games/GameForm.jsx`)
Formulaire d'ajout/modification de jeu

#### 7.3 GameProgress (`src/components/games/GameProgress.jsx`)
Progression du jeu (heures jouées / temps pour finir)

#### 7.4 GameSearch (`src/components/games/GameSearch.jsx`)
Recherche de jeux via HowLongToBeat

---

### Phase 8 : Custom Hooks

#### 8.1 useBooks (`src/hooks/useBooks.js`)
Hook personnalisé pour gérer les livres :
```js
const { books, loading, error, addBook, updateBook, deleteBook } = useBooks()
```

Encapsule :
- Fetch des données
- État de chargement
- Gestion des erreurs
- CRUD operations

#### 8.2 useGames (`src/hooks/useGames.js`)
Même logique pour les jeux

**Concepts clés :**
- Custom hooks commencent par `use`
- Réutilisabilité de la logique
- Séparation des préoccupations

---

### Phase 9 : shadcn/ui Components

Installer les composants shadcn/ui nécessaires :

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add input
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add progress
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add select
npx shadcn-ui@latest add form
```

Utiliser ces composants dans vos pages :
- `Button` pour les actions
- `Card` pour les cartes de livres/jeux
- `Dialog` pour les modales
- `Progress` pour les barres de progression
- `Badge` pour les status

**Concepts clés :**
- shadcn/ui copie les composants dans votre projet
- Personnalisables avec TailwindCSS
- Accessibles par défaut

---

### Phase 10 : State Management (optionnel)

Si l'app devient complexe, utiliser un state manager :

**Option 1 : Context API (simple)**
```js
// src/context/AppContext.jsx
const AppContext = createContext()

export const AppProvider = ({ children }) => {
  const [books, setBooks] = useState([])
  const [games, setGames] = useState([])
  
  return (
    <AppContext.Provider value={{ books, games, setBooks, setGames }}>
      {children}
    </AppContext.Provider>
  )
}
```

**Option 2 : Zustand (recommandé)**
```bash
npm install zustand
```

Plus simple que Redux, parfait pour des apps moyennes.

---

## Concepts React à maîtriser

### Components & Props
```jsx
function BookCard({ title, author, onClick }) {
  return (
    <div onClick={onClick}>
      <h3>{title}</h3>
      <p>{author}</p>
    </div>
  )
}
```

### State & Effects
```jsx
const [books, setBooks] = useState([])

useEffect(() => {
  fetchBooks().then(data => setBooks(data))
}, []) // [] = run once on mount
```

### Conditional Rendering
```jsx
{loading && <Spinner />}
{error && <ErrorMessage error={error} />}
{books.length > 0 && <BookList books={books} />}
```

### Lists & Keys
```jsx
{books.map(book => (
  <BookCard key={book.id} {...book} />
))}
```

### Forms
```jsx
const [title, setTitle] = useState('')

<input 
  value={title} 
  onChange={(e) => setTitle(e.target.value)} 
/>
```

---

## Styling avec TailwindCSS

### Classes utiles
```jsx
// Layout
<div className="flex flex-col gap-4 p-6">

// Grid
<div className="grid grid-cols-1 md:grid-cols-3 gap-4">

// Card
<div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition">

// Button
<button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">

// Responsive
<div className="text-sm md:text-base lg:text-lg">
```

---

## Dockerfile Frontend

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host"]
```

---

## Commandes utiles

### Développement
```bash
# Lancer le dev server
npm run dev

# Build pour production
npm run build

# Preview du build
npm run preview
```

### Avec Docker
```bash
# Lancer frontend + backend
docker-compose up

# Rebuild
docker-compose up --build

# Logs
docker-compose logs -f frontend
```

### Tests
```bash
# Installer Vitest
npm install -D vitest @testing-library/react @testing-library/jest-dom

# Lancer les tests
npm run test
```

---

## Ressources

- **React** : https://react.dev
- **Vite** : https://vitejs.dev
- **TailwindCSS** : https://tailwindcss.com
- **shadcn/ui** : https://ui.shadcn.com
- **React Router** : https://reactrouter.com
- **Lucide Icons** : https://lucide.dev

---

## Checklist de progression

- [ ] Phase 1 : Setup (Vite, TailwindCSS, shadcn/ui)
- [ ] Phase 2 : Configuration API (axios, services)
- [ ] Phase 3 : Routing (React Router)
- [ ] Phase 4 : Layout (Header, Sidebar)
- [ ] Phase 5 : Pages (Home, Books, Games, Stats)
- [ ] Phase 6 : Composants Books
- [ ] Phase 7 : Composants Games
- [ ] Phase 8 : Custom Hooks
- [ ] Phase 9 : shadcn/ui Components
- [ ] Phase 10 : State Management (si nécessaire)
- [ ] Tests : Tester toutes les fonctionnalités
- [ ] Polish : Animations, responsive, UX

---

## Bonnes pratiques

1. **Nommer les composants en PascalCase** : `BookCard.jsx`
2. **Nommer les fonctions en camelCase** : `fetchBooks()`
3. **Un composant = un fichier**
4. **Props destructuring** : `function Card({ title, author })`
5. **Utiliser les fragments** : `<>...</>` au lieu de `<div>`
6. **Keys uniques** dans les listes
7. **Éviter les inline functions** dans les renders (performance)
8. **Utiliser les custom hooks** pour la logique réutilisable
9. **Responsive first** avec TailwindCSS
10. **Accessibilité** : labels, aria-*, keyboard navigation
