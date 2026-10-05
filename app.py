import hashlib
import hmac
import os
import re
import secrets
import sqlite3
from datetime import timedelta
from functools import wraps
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort, Response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

SECRET_KEY = os.environ.get("SECRET_KEY")

# Production deployments must provide a strong SECRET_KEY.
# Tests/local development may use the non-secret fallback.
if not SECRET_KEY and os.environ.get("RENDER"):
    raise RuntimeError("SECRET_KEY must be set in production")

app.secret_key = SECRET_KEY or "dev-only-secret-key"
app.permanent_session_lifetime = timedelta(minutes=30)

app.config.update(
    SESSION_COOKIE_SECURE=not app.debug,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
# Trust Render/Cloudflare proxy headers so request.host_url reflects the public domain.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
_APP_DIR = os.path.dirname(os.path.abspath(__file__))


def resolve_database_path(base_dir=None):
    """Database file location. Set DB_DIR env var to a Render Persistent Disk
    mount path (e.g. /var/data) so data survives redeploys."""
    directory = base_dir or os.environ.get("DB_DIR", _APP_DIR)
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, "aizonabangla.db")


DATABASE = resolve_database_path()

CATEGORIES = ["AI Chat", "AI Writing", "AI Image", "AI Video", "AI Design"]

# ---------- DB helpers ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        url TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    """)
    # default admin
    cur = db.execute("SELECT COUNT(*) FROM admin")
    if cur.fetchone()[0] == 0:
        initial = os.environ.get("ADMIN_INITIAL_PASSWORD", "")
        if len(initial) < 12:
            initial = generate_secure_password()
        db.execute("INSERT INTO admin (username, password_hash) VALUES (?, ?)",
                   ("admin", generate_password_hash(initial)))
    # seed tools
    cur = db.execute("SELECT COUNT(*) FROM tools")
    if cur.fetchone()[0] == 0:
        seed_tools = [
            ("ChatGPT", "জনপ্রিয় AI চ্যাটবট। লেখা, কোডিং, প্রশ্নোত্তর সব কিছুর জন্য সেরা।", "AI Chat", "https://chat.openai.com"),
            ("Gemini", "Google-এর AI চ্যাট সহকারী। বাংলা ভাষায়ও ভালো উত্তর দেয়।", "AI Chat", "https://gemini.google.com"),
            ("Claude", "Anthropic-এর নিরাপদ ও বুদ্ধিমান AI চ্যাটবট।", "AI Chat", "https://claude.ai"),
            ("Jasper", "ব্লগ, মার্কেটিং কপি ও SEO লেখার জন্য AI রাইটিং টুল।", "AI Writing", "https://www.jasper.ai"),
            ("Copy.ai", "সহজে বাংলা ও ইংরেজিতে কনটেন্ট লেখার AI টুল।", "AI Writing", "https://www.copy.ai"),
            ("Midjourney", "টেক্সট থেকে অসাধারণ ছবি বানানোর AI টুল।", "AI Image", "https://www.midjourney.com"),
            ("DALL-E 3", "OpenAI-এর টেক্সট-টু-ইমেজ জেনারেটর।", "AI Image", "https://openai.com/dall-e-3"),
            ("Leonardo AI", "ফ্রি AI ছবি ও ডিজাইন তৈরির চমৎকার টুল।", "AI Image", "https://leonardo.ai"),
            ("Runway", "টেক্সট ও ছবি থেকে AI ভিডিও বানানোর সেরা প্ল্যাটফর্ম।", "AI Video", "https://runwayml.com"),
            ("Pictory", "লেখা থেকে স্বয়ংক্রিয়ভাবে ভিডিও তৈরি করে।", "AI Video", "https://pictory.ai"),
            ("Canva AI", "ডিজাইন, প্রেজেন্টেশন ও সোশ্যাল মিডিয়া পোস্টের জন্য AI ফিচারসহ।", "AI Design", "https://www.canva.com"),
            ("Adobe Firefly", "Adobe-এর AI ডিজাইন ও ইমেজ টুল।", "AI Design", "https://firefly.adobe.com"),
        ]
        db.executemany("INSERT INTO tools (name, description, category, url) VALUES (?,?,?,?)", seed_tools)
    # seed posts
    cur = db.execute("SELECT COUNT(*) FROM posts")
    if cur.fetchone()[0] == 0:
        seed_posts = [
            ("AI দিয়ে বাংলা ব্লগ লেখার ৫টি সহজ উপায়", "AI টুল ব্যবহার করে আপনি সহজেই বাংলা ব্লগ লিখতে পারেন।\n\n১. প্রথমে ChatGPT বা Gemini-তে বিষয় লিখুন।\n২. বাংলায় লিখতে বলুন।\n৩. খসড়া এডিট করুন।\n৪. Copy.ai দিয়ে শিরোনাম বানান।\n৫. Canva দিয়ে কভার ডিজাইন করুন।\n\nমনে রাখবেন: AI-এর লেখা সবসময় নিজে যাচাই করে প্রকাশ করবেন।"),
            ("ফ্রিতে AI ছবি বানানো শিখুন", "Leonardo AI বা Bing Image Creator দিয়ে ফ্রিতে ছবি বানাতে পারেন।\n\nধাপ ১: সাইটে ফ্রি অ্যাকাউন্ট খুলুন।\nধাপ ২: বাংলায় বা ইংরেজিতে prompt লিখুন, যেমন 'a beautiful village in Bangladesh, sunset'।\nধাপ ৩: Generate চাপুন ও ডাউনলোড করুন।"),
            ("AI ভিডিও বানিয়ে ইউটিউব থেকে আয়", "Pictory বা Runway দিয়ে স্ক্রিপ্ট থেকে ভিডিও বানিয়ে ইউটিউবে আপলোড করতে পারেন। ভয়েসওভারের জন্য ElevenLabs ব্যবহার করুন।"),
            ("ChatGPT vs Gemini vs Claude: বাংলায় কোন AI চ্যাটবট সেরা?",
             "তিনটি চ্যাটবটই বাংলায় উত্তর দেয়, তবে স্বাদ আলাদা।\n\nChatGPT: নির্দেশনা মানা ও লেখালেখিতে সবচেয়ে ভারসাম্যপূর্ণ। দৈনন্দিন কাজের জন্য নিরাপদ পছন্দ।\nGemini: Google সার্চ ও ইউটিউবের তথ্যের সাথে যুক্ত, সাম্প্রতিক বিষয়ে ভালো। গুগল অ্যাকাউন্ট থাকলে শুরু করা সবচেয়ে সহজ।\nClaude: লম্বা লেখা ও যত্নশীল উত্তরে এগিয়ে। গল্প, অনুবাদ ও এডিটিংয়ে আমার অভিজ্ঞতায় চমৎকার।\n\nপরামর্শ: একই প্রশ্ন তিনটিকে করে দেখুন, যার উত্তর আপনার কাজে লাগে সেটাই আপনার জন্য সেরা।"),
            ("ফেসবুক পেজের এক সপ্তাহের কনটেন্ট একদিনে বানান",
             "ছোট ব্যবসার পেজ চালাতে প্রতিদিন পোস্ট ভাবা কঠিন। AI দিয়ে একদিনেই সপ্তাহের কনটেন্ট তৈরি করুন।\n\nধাপ ১: ChatGPT-কে বলুন — আমার দোকান, কাস্টমার ও পণ্য সম্পর্কে ২ লাইন লিখে ৭ দিনের পোস্ট আইডিয়া চান।\nধাপ ২: প্রতিটি আইডিয়া থেকে ছোট ক্যাপশন লিখিয়ে নিন, বাংলায়।\nধাপ ৩: Canva AI দিয়ে প্রতিটি পোস্টের ছবি বানান।\nধাপ ৪: ফেসবুকের শিডিউল ফিচারে পুরো সপ্তাহের পোস্ট আগে থেকে সাজিয়ে রাখুন।\n\nমনে রাখবেন: দাম, অফার ও ঠিকানার মতো তথ্য নিজে মিলিয়ে নিন — AI ভুল লিখতে পারে।"),
            ("ছাত্রদের জন্য AI: পড়াশোনায় স্মার্ট ব্যবহার",
             "AI দিয়ে নোট, সারাংশ ও প্র্যাকটিস প্রশ্ন বানিয়ে পড়া দ্রুত করা যায়।\n\n১. কঠিন অধ্যায় পেস্ট করে সহজ ভাষায় বুঝিয়ে নিন।\n২. পরীক্ষার আগে সম্ভাব্য প্রশ্ন বানিয়ে নিজেকে যাচাই করুন।\n৩. ইংরেজি-বাংলা অনুবাদ করে শব্দভাণ্ডার বাড়ান।\n\nসতর্কতা: অ্যাসাইনমেন্ট হুবহু কপি করে জমা দেবেন না — শেখার জন্য ব্যবহার করুন, প্রতারণার জন্য নয়। AI-এর উত্তরে ভুল থাকতে পারে, বইয়ের সাথে মিলিয়ে নিন।"),
        ]
        db.executemany("INSERT INTO posts (title, content) VALUES (?,?)", seed_posts)
    db.commit()
    db.close()

def generate_secure_password(length=16):
    alphabet = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def retire_default_password():
    """Disable the old default password 'admin123' if it is still active."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    try:
        admin = db.execute("SELECT * FROM admin WHERE username = ?", ("admin",)).fetchone()
        if admin and check_password_hash(admin["password_hash"], "admin123"):
            db.execute("UPDATE admin SET password_hash = ? WHERE username = ?",
                       (generate_password_hash(generate_secure_password()), "admin"))
            db.commit()
    finally:
        db.close()


ADMIN_RESET_ENV_VAR = "ADMIN_RESET_PASSWORD"
ADMIN_RESET_MIN_LENGTH = 12


def apply_admin_reset_from_env(db_path=None):
    """One-time admin password reset driven by the ADMIN_RESET_PASSWORD env var.

    Returns "missing", "rejected:short", "no-admin", "already-applied" or "applied".
    The password and its hash are never logged or returned.
    """
    path = db_path or DATABASE
    new_password = os.environ.get(ADMIN_RESET_ENV_VAR, "")
    if not new_password:
        return "missing"
    if len(new_password) < ADMIN_RESET_MIN_LENGTH:
        app.logger.warning("Admin password reset rejected: password must be at least 12 characters.")
        return "rejected:short"
    fingerprint = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    try:
        db.execute("CREATE TABLE IF NOT EXISTS app_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
        admin = db.execute("SELECT * FROM admin WHERE username = ?", ("admin",)).fetchone()
        if not admin:
            app.logger.warning("Admin password reset skipped: admin user not found.")
            return "no-admin"
        row = db.execute("SELECT value FROM app_meta WHERE key = ?", ("admin_reset_fingerprint",)).fetchone()
        if row and row["value"] == fingerprint:
            return "already-applied"
        db.execute("UPDATE admin SET password_hash = ? WHERE username = ?",
                   (generate_password_hash(new_password), "admin"))
        db.execute("INSERT OR REPLACE INTO app_meta (key, value) VALUES (?, ?)",
                   ("admin_reset_fingerprint", fingerprint))
        db.commit()
        count = db.execute("SELECT COUNT(*) FROM admin").fetchone()[0]
        assert count == 1, "duplicate admin user detected"
        app.logger.warning("Admin password reset applied.")
        return "applied"
    finally:
        db.close()


# ---------- validation ----------
def valid_url(u):
    try:
        p = urlparse(u.strip())
        return p.scheme in ("http", "https") and "." in p.netloc
    except Exception:
        return False

def valid_email(e):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e or "") is not None

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("অনুগ্রহ করে লগইন করুন।", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def get_csrf_token():
    token = session.get("_csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


@app.context_processor
def inject_csrf_token():
    return {"csrf_token": get_csrf_token()}


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.before_request
def csrf_protect():
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        token = session.get("_csrf_token")
        submitted = request.form.get("_csrf_token") or request.headers.get("X-CSRF-Token")
        if not token or not submitted or not hmac.compare_digest(token, submitted):
            abort(400)



# ---------- public routes ----------
@app.route("/")
def index():
    db = get_db()
    tools = db.execute("SELECT * FROM tools ORDER BY id DESC LIMIT 6").fetchall()
    posts = db.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 3").fetchall()
    return render_template("index.html", tools=tools, posts=posts)

@app.route("/tools")
def tools():
    q = (request.args.get("q") or "").strip()[:100]
    cat = (request.args.get("category") or "").strip()
    db = get_db()
    query = "SELECT * FROM tools WHERE 1=1"
    params = []
    if cat and cat in CATEGORIES:
        query += " AND category = ?"
        params.append(cat)
    if q:
        query += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    query += " ORDER BY id DESC"
    tools = db.execute(query, params).fetchall()
    return render_template("tools.html", tools=tools, categories=CATEGORIES, q=q, selected_cat=cat)

@app.route("/tutorials")
def tutorials():
    return render_template("tutorials.html")

@app.route("/blog")
def blog():
    db = get_db()
    posts = db.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    return render_template("blog.html", posts=posts)

@app.route("/blog/<int:post_id>")
def blog_detail(post_id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if not post:
        abort(404)
    others = db.execute("SELECT * FROM posts WHERE id != ? ORDER BY id DESC LIMIT 3", (post_id,)).fetchall()
    return render_template("blog_detail.html", post=post, others=others)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()[:100]
        email = (request.form.get("email") or "").strip()[:100]
        message = (request.form.get("message") or "").strip()[:2000]
        if len(name) < 2:
            flash("সঠিক নাম লিখুন।", "error")
        elif not valid_email(email):
            flash("সঠিক ইমেইল দিন।", "error")
        elif len(message) < 5:
            flash("মেসেজ কমপক্ষে ৫ অক্ষরের হতে হবে।", "error")
        else:
            db = get_db()
            db.execute("INSERT INTO messages (name, email, message) VALUES (?,?,?)", (name, email, message))
            db.commit()
            flash("আপনার মেসেজ পাঠানো হয়েছে। ধন্যবাদ!", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html")

# ---------- SEO: robots.txt & sitemap.xml ----------
@app.route("/robots.txt")
def robots():
    lines = ["User-agent: *", "Allow: /", "Disallow: /admin", "Disallow: /login",
             f"Sitemap: {request.host_url}sitemap.xml"]
    return Response("\n".join(lines) + "\n", mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    db = get_db()
    posts = db.execute("SELECT id FROM posts ORDER BY id DESC").fetchall()
    urls = ["/", "/tools", "/tutorials", "/blog", "/about", "/contact"]
    urls += [f"/blog/{p['id']}" for p in posts]
    base = request.host_url.rstrip("/")
    items = "".join(f"<url><loc>{base}{u}</loc></url>" for u in urls)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>'
    return Response(xml, mimetype="application/xml")


# ---------- auth / admin ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()[:50]
        password = (request.form.get("password") or "")[:200]
        db = get_db()
        admin = db.execute("SELECT * FROM admin WHERE username = ?", (username,)).fetchone()
        if password == "admin123":
            flash("ডিফল্ট পাসওয়ার্ড নিষ্ক্রিয় করা হয়েছে। নতুন পাসওয়ার্ড ব্যবহার করুন।", "error")
        elif admin and check_password_hash(admin["password_hash"], password):
            session.clear()
            session["admin_logged_in"] = True
            session["admin_username"] = admin["username"]
            flash("স্বাগতম, " + admin["username"] + "!", "success")
            return redirect(url_for("admin_dashboard"))
        flash("ভুল ইউজারনেম বা পাসওয়ার্ড।", "error")
    return render_template("login.html")

@app.route("/admin/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current = (request.form.get("current_password") or "")[:200]
        new_pw = (request.form.get("new_password") or "")[:200]
        confirm = (request.form.get("confirm_password") or "")[:200]
        db = get_db()
        admin = db.execute("SELECT * FROM admin WHERE username = ?",
                           (session.get("admin_username"),)).fetchone()
        if not admin or not check_password_hash(admin["password_hash"], current):
            flash("বর্তমান পাসওয়ার্ড সঠিক নয়।", "error")
        elif new_pw != confirm:
            flash("নতুন পাসওয়ার্ড এবং কনফার্ম পাসওয়ার্ড মিলছে না।", "error")
        elif len(new_pw) < 12:
            flash("নতুন পাসওয়ার্ড কমপক্ষে ১২ অক্ষরের হতে হবে।", "error")
        elif current == new_pw:
            flash("নতুন পাসওয়ার্ড বর্তমান পাসওয়ার্ড থেকে আলাদা হতে হবে।", "error")
        else:
            db.execute("UPDATE admin SET password_hash = ? WHERE username = ?",
                       (generate_password_hash(new_pw), session.get("admin_username")))
            db.commit()
            flash("পাসওয়ার্ড সফলভাবে পরিবর্তন হয়েছে!", "success")
            return redirect(url_for("admin_dashboard"))
    return render_template("admin/change_password.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("লগআউট সফল হয়েছে।", "success")
    return redirect(url_for("index"))

@app.route("/admin")
@login_required
def admin_dashboard():
    db = get_db()
    tools = db.execute("SELECT * FROM tools ORDER BY id DESC").fetchall()
    posts = db.execute("SELECT * FROM posts ORDER BY id DESC").fetchall()
    messages = db.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 10").fetchall()
    counts = {
        "tools": db.execute("SELECT COUNT(*) FROM tools").fetchone()[0],
        "posts": db.execute("SELECT COUNT(*) FROM posts").fetchone()[0],
        "messages": db.execute("SELECT COUNT(*) FROM messages").fetchone()[0],
    }
    return render_template("admin/dashboard.html", tools=tools, posts=posts, messages=messages, counts=counts)

# tools CRUD
@app.route("/admin/tools/new", methods=["GET", "POST"])
@login_required
def tool_new():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()[:100]
        description = (request.form.get("description") or "").strip()[:2000]
        category = (request.form.get("category") or "").strip()
        url = (request.form.get("url") or "").strip()[:500]
        if len(name) < 2:
            flash("টুলের নাম কমপক্ষে ২ অক্ষর হতে হবে।", "error")
        elif len(description) < 5:
            flash("বর্ণনা কমপক্ষে ৫ অক্ষর হতে হবে।", "error")
        elif category not in CATEGORIES:
            flash("সঠিক ক্যাটাগরি বেছে নিন।", "error")
        elif not valid_url(url):
            flash("সঠিক website link দিন (https:// সহ)।", "error")
        else:
            db = get_db()
            db.execute("INSERT INTO tools (name, description, category, url) VALUES (?,?,?,?)", (name, description, category, url))
            db.commit()
            flash("টুল যোগ করা হয়েছে!", "success")
            return redirect(url_for("admin_dashboard"))
        return render_template("admin/tool_form.html", categories=CATEGORIES, tool=request.form, title="নতুন টুল যোগ করুন")
    return render_template("admin/tool_form.html", categories=CATEGORIES, tool={}, title="নতুন টুল যোগ করুন")

@app.route("/admin/tools/edit/<int:tool_id>", methods=["GET", "POST"])
@login_required
def tool_edit(tool_id):
    db = get_db()
    tool = db.execute("SELECT * FROM tools WHERE id = ?", (tool_id,)).fetchone()
    if not tool:
        abort(404)
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()[:100]
        description = (request.form.get("description") or "").strip()[:2000]
        category = (request.form.get("category") or "").strip()
        url = (request.form.get("url") or "").strip()[:500]
        if len(name) < 2:
            flash("টুলের নাম কমপক্ষে ২ অক্ষর হতে হবে।", "error")
        elif len(description) < 5:
            flash("বর্ণনা কমপক্ষে ৫ অক্ষর হতে হবে।", "error")
        elif category not in CATEGORIES:
            flash("সঠিক ক্যাটাগরি বেছে নিন।", "error")
        elif not valid_url(url):
            flash("সঠিক website link দিন (https:// সহ)।", "error")
        else:
            db.execute("UPDATE tools SET name=?, description=?, category=?, url=? WHERE id=?", (name, description, category, url, tool_id))
            db.commit()
            flash("টুল আপডেট হয়েছে!", "success")
            return redirect(url_for("admin_dashboard"))
        return render_template("admin/tool_form.html", categories=CATEGORIES, tool=request.form, title="টুল এডিট করুন")
    return render_template("admin/tool_form.html", categories=CATEGORIES, tool=tool, title="টুল এডিট করুন")

@app.route("/admin/tools/delete/<int:tool_id>", methods=["POST"])
@login_required
def tool_delete(tool_id):
    db = get_db()
    db.execute("DELETE FROM tools WHERE id = ?", (tool_id,))
    db.commit()
    flash("টুল ডিলিট করা হয়েছে।", "success")
    return redirect(url_for("admin_dashboard"))

# posts CRUD
@app.route("/admin/posts/new", methods=["GET", "POST"])
@login_required
def post_new():
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()[:200]
        content = (request.form.get("content") or "").strip()[:20000]
        if len(title) < 3:
            flash("শিরোনাম কমপক্ষে ৩ অক্ষর হতে হবে।", "error")
        elif len(content) < 10:
            flash("কনটেন্ট কমপক্ষে ১০ অক্ষর হতে হবে।", "error")
        else:
            db = get_db()
            db.execute("INSERT INTO posts (title, content) VALUES (?,?)", (title, content))
            db.commit()
            flash("ব্লগ পোস্ট যোগ হয়েছে!", "success")
            return redirect(url_for("admin_dashboard"))
        return render_template("admin/blog_form.html", post=request.form, title="নতুন ব্লগ পোস্ট")
    return render_template("admin/blog_form.html", post={}, title="নতুন ব্লগ পোস্ট")

@app.route("/admin/posts/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def post_edit(post_id):
    db = get_db()
    post = db.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    if not post:
        abort(404)
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()[:200]
        content = (request.form.get("content") or "").strip()[:20000]
        if len(title) < 3:
            flash("শিরোনাম কমপক্ষে ৩ অক্ষর হতে হবে।", "error")
        elif len(content) < 10:
            flash("কনটেন্ট কমপক্ষে ১০ অক্ষর হতে হবে।", "error")
        else:
            db.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, post_id))
            db.commit()
            flash("পোস্ট আপডেট হয়েছে!", "success")
            return redirect(url_for("admin_dashboard"))
        return render_template("admin/blog_form.html", post=request.form, title="পোস্ট এডিট করুন")
    return render_template("admin/blog_form.html", post=post, title="পোস্ট এডিট করুন")

@app.route("/admin/posts/delete/<int:post_id>", methods=["POST"])
@login_required
def post_delete(post_id):
    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    db.commit()
    flash("পোস্ট ডিলিট করা হয়েছে।", "success")
    return redirect(url_for("admin_dashboard"))

# Render/Gunicorn: DB init at import time (idempotent), so fresh deploys work.
# __main__ block below is only for local dev.
try:
    init_db()
    retire_default_password()
    apply_admin_reset_from_env()
except Exception:
    pass

@app.route("/quran")
def quran():
    lessons = [
        {
            "id": 1,
            "title": "আরবি হরফের পরিচয়",
            "level": "Level 0",
            "description": "কুরআন পড়া শেখার প্রথম ধাপ।"
        }
    ]
    return render_template("quran.html", lessons=lessons)


@app.route("/quran/lesson/<int:lesson_id>")
def quran_lesson(lesson_id):
    if lesson_id != 1:
        return "Lesson not found", 404

    letters = [
        ("ا", "আলিফ"),
        ("ب", "বা"),
        ("ت", "তা"),
        ("ث", "ছা"),
        ("ج", "জীম"),
        ("ح", "হা"),
        ("خ", "খা"),
        ("د", "দাল"),
        ("ذ", "যাল"),
        ("ر", "রা"),
        ("ز", "যায়"),
        ("س", "সীন"),
        ("ش", "শীন"),
        ("ص", "সাদ"),
        ("ض", "দাদ"),
        ("ط", "ত্বা"),
        ("ظ", "যা"),
        ("ع", "আইন"),
        ("غ", "গইন"),
        ("ف", "ফা"),
        ("ق", "ক্বাফ"),
        ("ك", "কাফ"),
        ("ل", "লাম"),
        ("م", "মীম"),
        ("ن", "নূন"),
        ("ه", "হা"),
        ("و", "ওয়াও"),
        ("ي", "ইয়া"),
    ]

    return render_template(
        "quran_lesson.html",
        lesson_id=lesson_id,
        letters=letters
    )


@app.route("/quran/lesson/2")
def quran_lesson_2():
    examples = [
        ("ب", "বা"),
        ("ت", "তা"),
        ("ث", "ছা"),
        ("ن", "নূন"),
        ("ي", "ইয়া"),
    ]

    return render_template(
        "quran_lesson_2.html",
        examples=examples
    )

@app.route("/quran/lesson/3")
def quran_lesson_3():
    harakat = [
        ("بَ", "যবর", "বা"),
        ("بِ", "যের", "বি"),
        ("بُ", "পেশ", "বু"),
        ("تَ", "যবর", "তা"),
        ("تِ", "যের", "তি"),
        ("تُ", "পেশ", "তু"),
    ]

    return render_template(
        "quran_lesson_3.html",
        harakat=harakat
    )

@app.route("/quran/lesson/4")
def quran_lesson_4():
    tanwin = [
        ("بً", "দুই যবর", "বান"),
        ("بٍ", "দুই যের", "বিন"),
        ("بٌ", "দুই পেশ", "বুন"),
        ("تً", "দুই যবর", "তান"),
        ("تٍ", "দুই যের", "তিন"),
        ("تٌ", "দুই পেশ", "তুন"),
    ]

    return render_template(
        "quran_lesson_4.html",
        tanwin=tanwin
    )

@app.route("/quran/lesson/5")
def quran_lesson_5():
    sukun = [
        ("اَ", "আলিফ + যবর"),
        ("بْ", "বা + সুকুন"),
        ("تْ", "তা + সুকুন"),
        ("نْ", "নূন + সুকুন"),
        ("مْ", "মীম + সুকুন"),
        ("لْ", "লাম + সুকুন"),
    ]

    return render_template(
        "quran_lesson_5.html",
        sukun=sukun
    )

@app.route("/quran/lesson/6")
def quran_lesson_6():
    shadda = [
        ("بَّ", "বা + শাদ্দাহ + যবর"),
        ("بِّ", "বা + শাদ্দাহ + যের"),
        ("بُّ", "বা + শাদ্দাহ + পেশ"),
        ("تَّ", "তা + শাদ্দাহ + যবর"),
        ("مِّ", "মীম + শাদ্দাহ + যের"),
        ("نُّ", "নূন + শাদ্দাহ + পেশ"),
    ]

    return render_template(
        "quran_lesson_6.html",
        shadda=shadda
    )

@app.route("/quran/lesson/7")
def quran_lesson_7():
    madd = [
        ("بَا", "বা — আলিফের মাধ্যমে দীর্ঘ"),
        ("بِي", "বি — ইয়ার মাধ্যমে দীর্ঘ"),
        ("بُو", "বু — ওয়াওয়ের মাধ্যমে দীর্ঘ"),
        ("تَا", "তা — আলিফের মাধ্যমে দীর্ঘ"),
        ("تِي", "তি — ইয়ার মাধ্যমে দীর্ঘ"),
        ("تُو", "তু — ওয়াওয়ের মাধ্যমে দীর্ঘ"),
    ]

    return render_template(
        "quran_lesson_7.html",
        madd=madd
    )

@app.route("/quran/lesson/8")
def quran_lesson_8():
    connected = [
        ("بَتَ", "বা-তা"),
        ("تَبَ", "তা-বা"),
        ("نَبَ", "না-বা"),
        ("مَنَ", "মা-না"),
        ("لَبَ", "লা-বা"),
        ("بَنَ", "বা-না"),
    ]

    return render_template(
        "quran_lesson_8.html",
        connected=connected
    )

@app.route("/quran/lesson/9")
def quran_lesson_9():
    positions = [
        ("ب", "আলাদা হরফ"),
        ("بـ", "শুরুর আকৃতি"),
        ("ـبـ", "মাঝের আকৃতি"),
        ("ـب", "শেষের আকৃতি"),
        ("م", "আলাদা হরফ"),
        ("مـ", "শুরুর আকৃতি"),
        ("ـمـ", "মাঝের আকৃতি"),
        ("ـم", "শেষের আকৃতি"),
    ]

    return render_template(
        "quran_lesson_9.html",
        positions=positions
    )

@app.route("/quran/lesson/10")
def quran_lesson_10():
    words = [
        ("بَابٌ", "বাবুন"),
        ("كِتَابٌ", "কিতাবুন"),
        ("قَلَمٌ", "কলামুন"),
        ("مَسْجِدٌ", "মাসজিদুন"),
        ("نَبِيٌّ", "নাবিয়্যুন"),
        ("رَسُولٌ", "রাসূলুন"),
    ]

    return render_template(
        "quran_lesson_10.html",
        words=words
    )

@app.route("/quran/lesson/11")
def quran_lesson_11():
    practice = [
        ("بَتَ", "বা-তা"),
        ("تَبَ", "তা-বা"),
        ("مَنَ", "মা-না"),
        ("نَبَ", "না-বা"),
        ("كَتَبَ", "কা-তা-বা"),
        ("دَخَلَ", "দা-খা-লা"),
        ("ذَهَبَ", "যা-হা-বা"),
        ("جَلَسَ", "জা-লা-সা"),
    ]

    return render_template(
        "quran_lesson_11.html",
        practice=practice
    )

@app.route("/quran/lesson/12")
def quran_lesson_12():
    rules = [
        ("الْ", "আলিফ-লাম — আলিফ-লাম পরিচয়"),
        ("الشَّمْسُ", "শামসিয়্যাহ উদাহরণ"),
        ("الْقَمَرُ", "কামারিয়্যাহ উদাহরণ"),
        ("بِالْكِتَابِ", "আলিফ-লামসহ শব্দ"),
        ("مِنَ الْبَيْتِ", "আলিফ-লামসহ বাক্যাংশ"),
        ("وَالْحَمْدُ", "আলিফ-লামসহ পরিচিত শব্দ"),
    ]

    return render_template(
        "quran_lesson_12.html",
        rules=rules
    )

@app.route("/quran/lesson/13")
def quran_lesson_13():
    examples = [
        ("بِسْمِ اللَّهِ", "বিসমিল্লাহর পরিচিতি"),
        ("رَبِّ", "রব্বি"),
        ("إِنَّ", "ইন্না"),
        ("ثُمَّ", "ছুম্মা"),
        ("مُحَمَّدٌ", "মুহাম্মাদুন"),
        ("اللَّهُ", "আল্লাহ"),
    ]

    return render_template(
        "quran_lesson_13.html",
        examples=examples
    )

@app.route("/quran/lesson/14")
def quran_lesson_14():
    examples = [
        ("قَالَ", "ক্বালা — আলিফের মাধ্যমে দীর্ঘ স্বর"),
        ("كَانَ", "কানা — আলিফের মাধ্যমে দীর্ঘ স্বর"),
        ("يَقُولُ", "ইয়াকূলু — ওয়াওয়ের মাধ্যমে দীর্ঘ স্বর"),
        ("قِيلَ", "ক্বীলা — ইয়ার মাধ্যমে দীর্ঘ স্বর"),
        ("فِي", "ফী — ইয়ার মাধ্যমে দীর্ঘ স্বর"),
        ("نُورٌ", "নূরুন — ওয়াওয়ের মাধ্যমে দীর্ঘ স্বর"),
    ]

    return render_template(
        "quran_lesson_14.html",
        examples=examples
    )

@app.route("/quran/lesson/15")
def quran_lesson_15():
    examples = [
        ("مِنْ", "মিন — সাকিন নূনের উদাহরণ"),
        ("أَنْ", "আন — সাকিন নূনের উদাহরণ"),
        ("مَنْ", "মান — সাকিন নূনের উদাহরণ"),
        ("عَنْ", "আন — সাকিন নূনের উদাহরণ"),
        ("مِنْهُ", "মিনহু — সাকিন নূনের অনুশীলন"),
        ("أَنْعَمَ", "আনআমা — সাকিন নূনের অনুশীলন"),
    ]
    return render_template("quran_lesson_15.html", examples=examples)

@app.route("/quran/lesson/16")
def quran_lesson_16():
    examples = [
        ("أَمْ", "আম্ — সাকিন মীমের উদাহরণ"),
        ("هُمْ", "হুম্ — সাকিন মীমের উদাহরণ"),
        ("عَلَيْهِمْ", "আলাইহিম্ — সাকিন মীমের অনুশীলন"),
        ("كَمْ", "কাম্ — সাকিন মীমের অনুশীলন"),
        ("أَنْتُمْ", "আনতুম্ — সাকিন মীমের অনুশীলন"),
        ("لَهُمْ", "লাহুম্ — সাকিন মীমের অনুশীলন"),
    ]
    return render_template("quran_lesson_16.html", examples=examples)

@app.route("/quran/lesson/17")
def quran_lesson_17():
    examples = [
        ("قَدْ", "ক্বাদ্ — ক্বলকলাহর উদাহরণ"),
        ("يَجْعَلْ", "ইয়াজআল্ — জীমের সাকিন অনুশীলন"),
        ("أَحَدْ", "আহাদ্ — দালের সাকিন অনুশীলন"),
        ("يَدْخُلْ", "ইয়াদখুল্ — দালের সাকিন অনুশীলন"),
        ("خَلَقْ", "খালাক্ — ক্বাফের সাকিন অনুশীলন"),
        ("وَتَبَّتْ", "ওয়া তাব্বাত্ — তায়ের সাকিন অনুশীলন"),
    ]
    return render_template("quran_lesson_17.html", examples=examples)

@app.route("/quran/lesson/18")
def quran_lesson_18():
    examples = [
        ("الْحَمْدُ", "আল-হামদু — পরিচিত কুরআনি শব্দ"),
        ("رَبِّ الْعَالَمِينَ", "রব্বিল আলামীন — পরিচিত বাক্যাংশ"),
        ("الرَّحْمَنِ", "আর-রহমান — শামসিয়্যাহ উদাহরণ"),
        ("الرَّحِيمِ", "আর-রহীম — শামসিয়্যাহ উদাহরণ"),
        ("مَالِكِ يَوْمِ الدِّينِ", "পরিচিত কুরআনি বাক্যাংশ"),
        ("إِيَّاكَ نَعْبُدُ", "পরিচিত কুরআনি বাক্যাংশ"),
    ]
    return render_template("quran_lesson_18.html", examples=examples)

@app.route("/quran/lesson/19")
def quran_lesson_19():
    examples = [
        ("وَقُلْ", "ওয়া কুল্ — থামা ও পড়ার অনুশীলন"),
        ("رَبِّ", "রব্বি — শাদ্দাহসহ শব্দ"),
        ("الْعَالَمِينَ", "আল-আলামীন — মাদ্দসহ শব্দ"),
        ("الرَّحِيمِ", "আর-রহীম — মাদ্দসহ শব্দ"),
        ("نَسْتَعِينُ", "নাস্তাঈনু — দীর্ঘ স্বরের অনুশীলন"),
        ("اهْدِنَا", "ইহদিনা — পরিচিত কুরআনি শব্দ"),
    ]
    return render_template("quran_lesson_19.html", examples=examples)

@app.route("/quran/lesson/20")
def quran_lesson_20():
    examples = [
        ("بِسْمِ اللَّهِ", "শুরু করার পরিচিত বাক্যাংশ"),
        ("الْحَمْدُ لِلَّهِ", "পরিচিত কুরআনি বাক্যাংশ"),
        ("رَبِّ الْعَالَمِينَ", "পরিচিত কুরআনি বাক্যাংশ"),
        ("الرَّحْمَنِ الرَّحِيمِ", "শামসিয়্যাহ ও মাদ্দ অনুশীলন"),
        ("مَالِكِ يَوْمِ الدِّينِ", "মাদ্দ ও শব্দজোড়া অনুশীলন"),
        ("إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ", "পূর্বের বিষয়গুলোর সমন্বিত অনুশীলন"),
    ]
    return render_template("quran_lesson_20.html", examples=examples)

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)