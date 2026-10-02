# AI Zone Bangla

Banglay AI shekhar website - Flask + SQLite.

## Feature
- Home, AI Tools, Tutorials, Blog, About, Contact page
- 5 category: AI Chat, AI Writing, AI Image, AI Video, AI Design
- Search + category filter
- Dark/Light mode
- Admin login + dashboard (tools/blog add/edit/delete)
- Security: password hashing, session protection, input validation

## Default Admin
- username: admin
- password: (প্রথম deploy-এ ADMIN_INITIAL_PASSWORD env variable থেকে সেট হয়; পরে /admin/change-password থেকে বদলান)

## Run
pip install -r requirements.txt
python app.py
Tarpor browser e jan: http://127.0.0.1:5000

## Admin password reset (Render / local)
- Set env variable `ADMIN_RESET_PASSWORD` (minimum 12 characters).
- On startup the app hashes it with Werkzeug and updates the `admin` user once.
- Same value will not reset again on restart (one-time fingerprint record).
- Short values are rejected with a generic log message; nothing secret is logged.
- After verifying login, remove the variable and redeploy.
