# Study Tracker — Minimal Frontend

A deliberately simple React frontend, built so you can focus on learning
**FastAPI** on the backend. No Redux, no Context API, no React Router,
no custom hooks, no CSS frameworks, no TypeScript — just plain
functional components and `useState`.

This app behaves like a simple client that consumes your future API.
Every action a user takes maps to one FastAPI endpoint you'll build.

## Folder structure

```
study-tracker-frontend/
├── index.html              # HTML entry point
├── package.json
├── vite.config.js
└── src/
    ├── main.jsx             # Renders <App /> into the page
    ├── App.jsx              # Holds ALL global state, switches between pages
    ├── App.css              # Plain CSS, no frameworks
    ├── api/
    │   └── api.js             # <-- ALL backend communication goes here
    ├── data/
    │   └── mockData.js        # Fake data used until your backend exists
    └── pages/
        ├── LoginPage.jsx
        ├── RegisterPage.jsx
        └── DashboardPage.jsx   # Welcome message, logout, add/edit/delete sessions
```

Only 3 pages now — the "Add Session" form lives inside `DashboardPage.jsx`
instead of being a separate page.

## State flow

All state lives in **`App.jsx`** and nowhere else:

| State          | What it holds                                   |
|-----------------|--------------------------------------------------|
| `currentPage`   | `"login"`, `"register"`, or `"dashboard"`        |
| `currentUser`   | The logged-in user object, or `null`             |
| `sessions`      | The array of study sessions                      |

`App.jsx` passes this state down to pages as **props**, along with
functions like `onAddSession`. Pages call those functions instead of
changing the data themselves. This is "one-way data flow":

```
App.jsx (state)
   │  props (data + functions)
   ▼
LoginPage / RegisterPage / DashboardPage
   │  calls onXxx(...) functions passed in from App.jsx
   ▼
App.jsx updates its state
   │
   ▼
Page re-renders with new data
```

`DashboardPage.jsx` also has a *little* of its own state (the text in
the add/edit form, and which session is currently being edited). That's
just local UI state for the form — it isn't shared with other pages,
so it's fine to keep it there instead of in `App.jsx`.

## Which action calls which FastAPI endpoint

All of this happens inside **`src/api/api.js`** — that's the only file
that should ever call `fetch()`. Pages call these functions; they never
talk to the network directly.

| Frontend action                          | Function in `api.js`   | FastAPI endpoint         |
|-------------------------------------------|--------------------------|----------------------------|
| Clicking "Register"                       | `registerUser()`        | `POST /register`          |
| Clicking "Login"                          | `loginUser()`            | `POST /login`             |
| (after login, loading the dashboard)      | `getSessions()`          | `GET /sessions`           |
| Submitting the form in "add" mode         | `addSession()`           | `POST /sessions`          |
| Submitting the form in "edit" mode        | `updateSession()`        | `PATCH /sessions/{id}`    |
| Clicking "Delete" on a session             | `deleteSession()`        | `DELETE /sessions/{id}`   |
| *(not wired up to a button yet)*          | `getCurrentUser()`       | `GET /me`                 |

Every function in `api.js` is labeled with a comment like:

```js
// FastAPI Endpoint:
// POST /register
```

and has the real `fetch()` call written out in a comment directly
above the mock line, ready to uncomment once your backend exists.
There's also a `BASE_URL` constant near the top of `api.js` — update
it if your FastAPI server runs somewhere other than
`http://127.0.0.1:8000`.

## How to run it
 
1. Make sure you have [Node.js](https://nodejs.org) installed.
2. From inside the `study-tracker-frontend` folder, run:
   ```
   npm install
   npm run dev
   ```
3. Open the URL shown in the terminal (usually `http://localhost:5173`).

You can log in with any email/password right now, add/edit/delete
sessions, and log out — it's all mocked, nothing is saved permanently.

## What's intentionally NOT included

- No authentication/JWT logic
- No real database — `src/data/mockData.js` stands in for it
- No React Router, Context API, Redux, or custom hooks
- No CSS framework, no TypeScript
- No animations or transitions

## Connecting your real backend later

Work through `src/api/api.js` function by function:
1. Uncomment the `fetch()` call.
2. Delete (or comment out) the mock line below it.
3. Confirm `BASE_URL` matches where your FastAPI server runs.

Nothing else in the app needs to change — pages already call these
functions and just use whatever they return.
