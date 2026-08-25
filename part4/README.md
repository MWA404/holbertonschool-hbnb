# Part 4 — Simple Web Client

The front-end of the HBnB application, built with HTML5, CSS3, and vanilla JavaScript (ES6). It consumes the Part 3 REST API.

## Pages

| File | Purpose |
|---|---|
| `index.html` | Lists all places with a client-side price filter |
| `login.html` | User login form (stores the JWT in a cookie) |
| `place.html` | Place details, amenities, and reviews |
| `add_review.html` | Review form, available to authenticated users only |

## Running

1. Start the Part 3 API first:
```bash
   cd ../part3
   python3 run.py
```
   The API runs on `http://127.0.0.1:5005`.

2. Serve this folder with a local web server (for example the VS Code Live Server
   extension) and open `index.html`.

## Notes

- The JWT returned by `/api/v1/auth/login` is stored in a cookie named `token`
  and sent in the `Authorization: Bearer <token>` header on protected requests.
- The price filter (10 / 50 / 100 / All) runs entirely client-side, with no page reload.
