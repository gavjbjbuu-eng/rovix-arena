from flask import Flask, redirect, render_template_string, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, login_required, current_user, LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xynos_ultimate_esports_key_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///xynos_pro_v18.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    ff_uid = db.Column(db.String(50), unique=True, nullable=False)
    wallet = db.Column(db.Integer, default=0)
    winnings = db.Column(db.Integer, default=0)
    role = db.Column(db.String(20), default='user')
    profile_pic = db.Column(db.String(500), default='https://api.dicebear.com/7.x/bottts/svg?seed=xynos')
    is_banned = db.Column(db.Boolean, default=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    game_mode = db.Column(db.String(50), nullable=False)
    map_name = db.Column(db.String(50), nullable=False)
    prize = db.Column(db.String(50), nullable=False)
    entry_fee = db.Column(db.Integer, default=0)
    room_id = db.Column(db.String(50), default="Awaiting Room ID")
    room_pass = db.Column(db.String(50), default="Awaiting Password")
    status = db.Column(db.String(20), default="Open")
    winner_info = db.Column(db.String(200), default="Yet to be declared")

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    utr_no = db.Column(db.String(20), unique=True, nullable=True)
    status = db.Column(db.String(20), default="Pending")

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    match_id = db.Column(db.Integer, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        db.session.add(User(username="admin", phone="9999999999", email="admin@xynos.com", password="adminpassword", ff_uid="XYNOS_ADMIN", wallet=0, winnings=5000, role="admin"))
        db.session.add(User(username="host_pro", phone="8888888888", email="host@xynos.com", password="hostpassword", ff_uid="XYNOS_HOST", wallet=0, winnings=1200, role="host"))
        db.session.commit()
    if not Match.query.first():
        db.session.add(Match(title="Free Fire Pro Clash Squad #1", game_mode="CS 4v4", map_name="Bermuda", prize="₹1,000", entry_fee=20, room_id="XYNOS-9982", room_pass="PRO2026", winner_info="Player_X won ₹1,000 (Top Killer)"))
        db.session.add(Match(title="Free Fire 1v1 Ultimate Faceoff", game_mode="CS 1v1", map_name="Factory", prize="₹400", entry_fee=15, room_id="XYNOS-1142", room_pass="1V1PRO", winner_info="Yet to be declared"))
        db.session.add(Match(title="Free Fire Bermuda Mega BR", game_mode="BR", map_name="Bermuda Full", prize="₹2,500", entry_fee=50, room_id="Awaiting Room ID", room_pass="Awaiting Password", winner_info="Yet to be declared"))
        db.session.add(Match(title="Lone Wolf Pro Clash", game_mode="Lone Wolf", map_name="Iron Cage", prize="₹600", entry_fee=20, room_id="Awaiting Room ID", room_pass="Awaiting Password", winner_info="Yet to be declared"))
        db.session.commit()

BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XYNOS_X ESPORTS</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800;900&display=swap');
        body { font-family: 'Outfit', sans-serif; }
        .glow-red { box-shadow: 0 0 25px rgba(239, 68, 68, 0.4); }
        .glow-gold { box-shadow: 0 0 20px rgba(234, 179, 8, 0.35); }
        .glass-card { background: linear-gradient(135deg, rgba(20, 20, 25, 0.95) 0%, rgba(10, 10, 15, 0.99) 100%); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); }
        @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
        .animate-marquee { display: inline-block; animation: marquee 16s linear infinite; }
    </style>
</head>
<body class="bg-[#040406] text-slate-100 min-h-screen pb-28 selection:bg-red-600 selection:text-white">
    <div class="fixed top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-red-600/15 rounded-full blur-[130px] pointer-events-none"></div>

    <nav class="bg-[#070709]/95 backdrop-blur-2xl border-b border-white/5 px-4 py-3.5 flex justify-between items-center sticky top-0 z-50 shadow-2xl">
        <a href="/home" class="flex items-center gap-2 group">
            <div class="bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 text-white font-black px-3.5 py-2 rounded-xl text-xs tracking-wider shadow-lg glow-red flex items-center gap-2">
                <span class="animate-pulse text-base">🔥</span> <span class="text-sm tracking-widest font-black">XYNOS_X</span>
            </div>
        </a>
        <div class="flex items-center gap-2 text-xs">
            {% if current_user.is_authenticated %}
                <div class="glass-card px-2.5 py-1.5 rounded-xl text-yellow-400 font-black flex items-center gap-1 glow-gold">
                    <span>🪙</span> ₹{{ current_user.wallet }}
                </div>
                <a href="/wallet" class="bg-emerald-500/10 text-emerald-400 px-2.5 py-1.5 rounded-xl font-bold border border-emerald-500/20">Wallet</a>
                {% if current_user.role in ['admin', 'host'] %}
                    <a href="/host-panel" class="bg-indigo-500/20 text-indigo-400 px-2.5 py-1.5 rounded-xl font-bold border border-indigo-500/20">Host</a>
                {% endif %}
                {% if current_user.role == 'admin' %}
                    <a href="/admin-panel" class="bg-purple-500/20 text-purple-400 px-2.5 py-1.5 rounded-xl font-bold border border-purple-500/20">Admin</a>
                {% endif %}
                <a href="/logout" class="bg-red-500/10 text-red-400 p-2 rounded-xl border border-red-500/20">🚪</a>
            {% else %}
                <a href="/login" class="bg-gradient-to-r from-red-600 to-rose-600 px-3.5 py-1.5 rounded-xl font-bold text-white shadow-lg glow-red">Login</a>
                <a href="/register" class="glass-card px-3.5 py-1.5 rounded-xl font-bold text-slate-200 border border-white/10">Register</a>
            {% endif %}
        </div>
    </nav>

    <div class="max-w-md mx-auto p-4 relative z-10">
        {{ content|safe }}
    </div>

    <div class="fixed bottom-2 left-3 right-3 bg-[#08080acc]/95 backdrop-blur-3xl border border-white/10 px-2 py-2 z-50 flex justify-around items-center max-w-md mx-auto rounded-2xl shadow-[0_15px_35px_rgba(0,0,0,0.9)]">
        <a href="/home" class="flex flex-col items-center gap-0.5 text-slate-400 hover:text-red-500 transition px-3 py-1 rounded-xl">
            <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
            <span class="text-[9px] font-extrabold uppercase tracking-widest">Home</span>
        </a>
        <a href="/games" class="flex flex-col items-center gap-0.5 text-slate-400 hover:text-red-500 transition px-3 py-1 rounded-xl">
            <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-10 7H8v3H6v-3H3v-2h3V8h2v3h3v2zm4.5 2c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm3-4c-.83 0-1.5-.67-1.5-1.5S19.67 8 20.5 8s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/></svg>
            <span class="text-[9px] font-extrabold uppercase tracking-widest">Tourneys</span>
        </a>
        <a href="/results" class="flex flex-col items-center gap-0.5 text-slate-400 hover:text-yellow-400 transition px-3 py-1 rounded-xl">
            <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
            <span class="text-[9px] font-extrabold uppercase tracking-widest">Results</span>
        </a>
        <a href="/support" class="flex flex-col items-center gap-0.5 text-slate-400 hover:text-emerald-400 transition px-3 py-1 rounded-xl">
            <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H7c0-2.76 2.24-5 5-5s5 2.24 5 5c0 1.03-.42 1.98-1.07 2.75z"/></svg>
            <span class="text-[9px] font-extrabold uppercase tracking-widest">Support</span>
        </a>
        <a href="/profile" class="flex flex-col items-center gap-0.5 text-slate-400 hover:text-indigo-400 transition px-3 py-1 rounded-xl">
            <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
            <span class="text-[9px] font-extrabold uppercase tracking-widest">Profile</span>
        </a>
    </div>
</body>
</html>
"""

@app.route('/')
def splash():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="UTF-8"><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-[#040406] text-white h-screen flex flex-col items-center justify-center p-4">
        <div class="w-full max-w-sm rounded-3xl overflow-hidden shadow-[0_0_50px_rgba(239,68,68,0.4)] border border-red-500/50 mb-6 bg-gradient-to-br from-red-950 via-zinc-900 to-black p-8 text-center">
            <div class="text-4xl mb-3 animate-bounce">🔥</div>
            <h1 class="text-xl font-black text-white tracking-wider">XYNOS_X ESPORTS</h1>
        </div>
        <div class="bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 text-white font-black px-8 py-3.5 rounded-2xl text-lg shadow-2xl animate-pulse tracking-wider">LOADING ARENA...</div>
        <script>setTimeout(() => { window.location.href = "/home"; }, 1500);</script>
    </body>
    </html>
    """

@app.route('/home')
def index():
    content = """
    <!-- Ticker -->
    <div class="mb-4 bg-gradient-to-r from-red-950/60 via-zinc-900 to-black border border-red-500/30 rounded-2xl px-3.5 py-2.5 overflow-hidden shadow-lg flex items-center gap-2">
        <span class="bg-red-600 text-white text-[9px] font-black px-2 py-0.5 rounded-md uppercase tracking-wider animate-pulse flex-shrink-0">⚡ Live</span>
        <div class="overflow-hidden whitespace-nowrap w-full">
            <p class="text-xs text-slate-300 font-bold animate-marquee">🔥 Daily Free Fire Clash Squad, 1v1 & Lone Wolf Tourneys Live! Check Results tab for winner declarations!</p>
        </div>
    </div>

    <!-- Stunning Guaranteed Visual Banner (No Broken Image Links) -->
    <div class="mb-5 relative rounded-3xl overflow-hidden shadow-[0_20px_50px_rgba(239,68,68,0.35)] border border-red-500/50 bg-gradient-to-r from-red-950 via-zinc-900 to-black p-6">
        <div class="absolute -right-6 -bottom-6 w-36 h-36 bg-red-600/30 rounded-full blur-2xl pointer-events-none"></div>
        <div class="relative z-10 flex flex-col space-y-3">
            <div class="flex items-center justify-between">
                <span class="bg-gradient-to-r from-red-600 to-rose-600 text-white text-[9px] font-black px-3 py-1 rounded-full uppercase tracking-widest shadow-lg glow-red">👑 PRO BATTLEGROUND</span>
                <span class="text-[9px] text-yellow-400 font-extrabold bg-yellow-500/20 px-2.5 py-1 rounded-lg border border-yellow-500/30">⚡ Instant Payout</span>
            </div>
            <div>
                <h1 class="text-lg font-black text-white tracking-wide uppercase">
                    XYNOS_X <span class="text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-rose-500 to-orange-400">ESPORTS ARENA</span>
                </h1>
                <p class="text-[11px] text-slate-300 mt-1">Play Free Fire custom tournaments, win cash prizes instantly & dominate the leaderboard!</p>
            </div>
        </div>
    </div>

    <div class="grid grid-cols-2 gap-3 mb-5">
        <a href="/games" class="bg-gradient-to-r from-red-600 via-rose-600 to-orange-600 text-white p-3.5 rounded-2xl font-black text-center shadow-lg glow-red text-xs">🎮 Play Tourneys</a>
        <a href="/results" class="glass-card text-yellow-400 p-3.5 rounded-2xl font-black text-center text-xs border border-yellow-500/30 flex items-center justify-center gap-1">🏆 Match Results</a>
    </div>

    <!-- Game Modes List -->
    <div class="space-y-3">
        <div class="flex items-center justify-between px-1">
            <h2 class="text-xs font-black text-red-500 uppercase tracking-widest flex items-center gap-1.5"><span>⚡</span> Free Fire Game Modes</h2>
            <a href="/results" class="text-[10px] text-yellow-400 font-extrabold bg-yellow-500/10 px-2.5 py-1 rounded-xl border border-yellow-500/20">View Results &rarr;</a>
        </div>
        
        <a href="/games?mode=CS 4v4" class="block glass-card hover:border-red-500/60 p-4 rounded-2xl transition shadow-xl relative overflow-hidden">
            <div class="flex items-center justify-between relative z-10">
                <div class="flex items-center gap-3.5">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-red-600/20 to-rose-600/30 text-red-400 font-black border border-red-500/30 flex items-center justify-center text-xl shadow-inner">⚡</div>
                    <div>
                        <span class="bg-red-500/20 text-red-400 text-[9px] px-2 py-0.5 rounded font-extrabold uppercase tracking-wider">Squad</span>
                        <h3 class="text-xs font-black text-white mt-1">Free Fire Clash Squad (CS 4v4)</h3>
                        <p class="text-[10px] text-slate-400 mt-0.5">Custom Room • Per Kill Bounty</p>
                    </div>
                </div>
                <span class="text-slate-500 text-sm font-bold">&rarr;</span>
            </div>
        </a>

        <a href="/games?mode=CS 1v1" class="block glass-card hover:border-orange-500/60 p-4 rounded-2xl transition shadow-xl relative overflow-hidden">
            <div class="flex items-center justify-between relative z-10">
                <div class="flex items-center gap-3.5">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-orange-600/20 to-amber-600/30 text-orange-400 font-black border border-orange-500/30 flex items-center justify-center text-xl shadow-inner">🎯</div>
                    <div>
                        <span class="bg-orange-500/20 text-orange-400 text-[9px] px-2 py-0.5 rounded font-extrabold uppercase tracking-wider">Faceoff</span>
                        <h3 class="text-xs font-black text-white mt-1">Free Fire CS 1v1</h3>
                        <p class="text-[10px] text-slate-400 mt-0.5">1v1 Clash • Custom Room</p>
                    </div>
                </div>
                <span class="text-slate-500 text-sm font-bold">&rarr;</span>
            </div>
        </a>

        <a href="/games?mode=BR" class="block glass-card hover:border-blue-500/60 p-4 rounded-2xl transition shadow-xl relative overflow-hidden">
            <div class="flex items-center justify-between relative z-10">
                <div class="flex items-center gap-3.5">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-600/20 to-cyan-600/30 text-blue-400 font-black border border-blue-500/30 flex items-center justify-center text-xl shadow-inner">🛡️</div>
                    <div>
                        <span class="bg-blue-500/20 text-blue-400 text-[9px] px-2 py-0.5 rounded font-extrabold uppercase tracking-wider">Survival</span>
                        <h3 class="text-xs font-black text-white mt-1">Free Fire Battle Royale (BR)</h3>
                        <p class="text-[10px] text-slate-400 mt-0.5">Bermuda / Purgatory • Massive Rewards</p>
                    </div>
                </div>
                <span class="text-slate-500 text-sm font-bold">&rarr;</span>
            </div>
        </a>

        <a href="/games?mode=Lone Wolf" class="block glass-card hover:border-purple-500/60 p-4 rounded-2xl transition shadow-xl relative overflow-hidden">
            <div class="flex items-center justify-between relative z-10">
                <div class="flex items-center gap-3.5">
                    <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-purple-600/20 to-indigo-600/30 text-purple-400 font-black border border-purple-500/30 flex items-center justify-center text-xl shadow-inner">🐺</div>
                    <div>
                        <span class="bg-purple-500/20 text-purple-400 text-[9px] px-2 py-0.5 rounded font-extrabold uppercase tracking-wider">Duel</span>
                        <h3 class="text-xs font-black text-white mt-1">Lone Wolf Pro Clash</h3>
                        <p class="text-[10px] text-slate-400 mt-0.5">Iron Cage • Direct Duel • Instant Payout</p>
                    </div>
                </div>
                <span class="text-slate-500 text-sm font-bold">&rarr;</span>
            </div>
        </a>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route('/games')
def games_section():
    selected_mode = request.args.get('mode', 'All')
    matches = Match.query.all() if selected_mode == 'All' else Match.query.filter_by(game_mode=selected_mode).all()
    joined_matches = [r.match_id for r in Registration.query.filter_by(user_id=current_user.id)] if current_user.is_authenticated else []
    modes = ['All', 'CS 4v4', 'CS 1v1', 'BR', 'Lone Wolf']

    inner_content = """
    <div class="mb-4 flex items-center justify-between">
        <h1 class="text-sm font-black text-red-500 uppercase tracking-wider flex items-center gap-1.5"><span>⚡</span> Tournaments Lobby</h1>
        <a href="/results" class="text-xs glass-card text-yellow-400 px-3 py-1.5 rounded-xl font-bold border border-yellow-500/30">🏆 View Results</a>
    </div>

    <div class="flex gap-2 overflow-x-auto pb-3 mb-4 scrollbar-none">
        {% for m in modes %}
        <a href="/games?mode={{ m }}" class="px-3.5 py-2 rounded-xl text-xs font-extrabold whitespace-nowrap transition {% if selected_mode == m %}bg-gradient-to-r from-red-600 to-rose-600 text-white shadow-lg glow-red{% else %}glass-card text-slate-400 border border-white/5{% endif %}">
            {{ m }}
        </a>
        {% endfor %}
    </div>

    <div class="space-y-3.5">
        {% for m in matches %}
        <div class="glass-card p-4 rounded-2xl shadow-xl relative overflow-hidden border border-white/10">
            <div class="absolute top-0 right-0 bg-gradient-to-l from-red-600/30 to-transparent text-red-400 text-[10px] px-3.5 py-1 rounded-bl-2xl font-black uppercase">
                {{ m.game_mode }}
            </div>
            <div>
                <span class="bg-emerald-500/15 text-emerald-400 text-[10px] px-2.5 py-0.5 rounded-full font-extrabold uppercase">{{ m.status }}</span>
                <h3 class="text-sm font-black mt-2.5 text-white">{{ m.title }}</h3>
                <p class="text-slate-400 text-xs mt-1">Map: <span class="text-slate-200 font-semibold">{{ m.map_name }}</span></p>
            </div>

            <div class="mt-3.5 pt-3.5 border-t border-white/5 flex justify-between items-center text-xs">
                <div>
                    <span class="text-slate-500 block text-[9px] font-bold">PRIZE POOL</span>
                    <span class="text-yellow-400 font-black text-sm">{{ m.prize }}</span>
                </div>
                <div>
                    <span class="text-slate-500 block text-[9px] font-bold">ENTRY FEE</span>
                    <span class="text-emerald-400 font-black">₹{{ m.entry_fee }}</span>
                </div>
            </div>

            <div class="mt-3.5 space-y-2">
                {% if current_user.is_authenticated %}
                    {% if m.id in joined_matches %}
                        <div class="bg-black/90 p-3 rounded-xl border border-emerald-500/40 text-xs space-y-1">
                            <span class="text-emerald-400 font-black uppercase text-[10px]">🔓 Room Credentials:</span>
                            <p class="text-slate-300 font-mono">ID: <span class="text-white">{{ m.room_id }}</span> | Pass: <span class="text-emerald-400">{{ m.room_pass }}</span></p>
                        </div>
                    {% else %}
                        {% if current_user.wallet >= m.entry_fee %}
                            <form action="/join/{{ m.id }}" method="POST">
                                <button type="submit" class="w-full bg-gradient-to-r from-red-600 to-rose-600 text-white font-black py-3 rounded-xl shadow-lg glow-red text-xs">Join Slot (₹{{ m.entry_fee }})</button>
                            </form>
                        {% else %}
                            <a href="/wallet" class="block text-center bg-red-950/40 border border-red-500/40 text-red-400 py-3 rounded-xl font-bold text-xs">Insufficient Funds (Add via UPI)</a>
                        {% endif %}
                    {% endif %}
                {% else %}
                    <a href="/login" class="block text-center glass-card text-slate-200 py-3 rounded-xl font-bold text-xs">Login to Join</a>
                {% endif %}
                <div class="text-[10px] bg-yellow-500/10 text-yellow-400 p-2 rounded-xl border border-yellow-500/20 font-bold">
                    🏆 Result: {{ m.winner_info }}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    """
    return render_template_string(BASE_HTML, content=render_template_string(inner_content, matches=matches, modes=modes, selected_mode=selected_mode, joined_matches=joined_matches))

@app.route('/results')
def match_results():
    matches = Match.query.all()
    inner_content = """
    <div class="glass-card border border-white/10 p-6 rounded-2xl shadow-2xl space-y-4 text-xs">
        <div>
            <span class="bg-yellow-500/15 text-yellow-400 text-[9px] font-black px-2.5 py-0.5 rounded uppercase border border-yellow-500/20">Official Announcements</span>
            <h2 class="text-sm font-black text-white mt-1.5 uppercase tracking-wider">🏆 Tournament Match Results</h2>
        </div>
        <div class="space-y-3">
            {% for m in matches %}
            <div class="bg-black/60 p-4 rounded-xl border border-white/5 space-y-2">
                <div class="flex justify-between items-center">
                    <span class="font-black text-white text-sm">{{ m.title }}</span>
                    <span class="text-[10px] text-red-400 bg-red-600/20 px-2 py-0.5 rounded font-bold">{{ m.game_mode }}</span>
                </div>
                <p class="text-slate-400 text-[11px]">Map: <span class="text-slate-200">{{ m.map_name }}</span> | Prize: <span class="text-yellow-400 font-bold">{{ m.prize }}</span></p>
                <div class="bg-emerald-500/10 p-2.5 rounded-lg border border-emerald-500/20 text-emerald-400 font-bold">
                    Winner/Status: {{ m.winner_info }}
                </div>
            </div>
            {% endfor %}
        </div>
        <a href="/home" class="block text-center glass-card text-slate-200 py-3 rounded-xl font-bold border border-white/10">&larr; Back to Home</a>
    </div>
    """
    return render_template_string(BASE_HTML, content=render_template_string(inner_content, matches=matches))

@app.route('/wallet', methods=['GET', 'POST'])
@login_required
def wallet():
    msg = ""
    error = ""
    if request.method == 'POST':
        action = request.form.get('action')
        amount = int(request.form.get('amount', 0))
        if action == 'deposit' and amount > 0:
            utr = request.form.get('utr_no', '').strip()
            if not utr or len(utr) != 12 or not utr.isdigit():
                error = "Invalid UTR! Must be exactly 12 digits."
            elif Transaction.query.filter_by(utr_no=utr).first():
                error = "UTR already used!"
            else:
                db.session.add(Transaction(user_id=current_user.id, amount=amount, type="Auto-Deposit", utr_no=utr, status="Success"))
                current_user.wallet += amount
                db.session.commit()
                msg = f"₹{amount} added successfully!"

    inner_content = """
    <div class="glass-card border border-white/10 p-6 rounded-2xl shadow-2xl space-y-4 text-xs">
        <h2 class="text-sm font-black text-emerald-400 uppercase tracking-wider">💳 Wallet & Auto UPI Deposit</h2>
        <div class="bg-black/60 p-4 rounded-xl border border-white/5 flex justify-between items-center">
            <span class="text-slate-400">Balance:</span>
            <span class="text-yellow-400 font-black text-base">₹{{ current_user.wallet }}</span>
        </div>
        {% if msg %}<div class="bg-emerald-500/20 text-emerald-400 p-3 rounded-xl border border-emerald-500/30 font-bold">{{ msg }}</div>{% endif %}
        {% if error %}<div class="bg-red-500/20 text-red-400 p-3 rounded-xl border border-red-500/30 font-bold">{{ error }}</div>{% endif %}

        <div class="bg-black/60 p-4 rounded-xl border border-white/5 text-center space-y-3">
            <p class="font-bold text-slate-300">Scan QR to Pay via UPI</p>
            <div class="bg-white p-3 inline-block rounded-2xl shadow-xl">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=upi://pay?pa=8298363286@mbkns&pn=XYNOS_X" class="mx-auto rounded" alt="QR">
            </div>
            <div class="bg-zinc-900 p-2 rounded-xl text-emerald-400 font-bold font-mono">UPI: 8298363286@mbkns</div>
        </div>

        <form method="POST" class="bg-black/60 p-4 rounded-xl border border-white/5 space-y-3">
            <input type="hidden" name="action" value="deposit">
            <input type="number" name="amount" placeholder="Amount (₹)" required class="w-full bg-black border border-white/10 rounded-xl p-3 text-white focus:outline-none">
            <input type="text" name="utr_no" placeholder="UPI UTR (12 digits)" maxlength="12" required class="w-full bg-black border border-white/10 rounded-xl p-3 text-white focus:outline-none">
            <button type="submit" class="w-full bg-emerald-600 font-bold py-3 rounded-xl text-white shadow-lg">Verify & Add Instantly</button>
        </form>
        <a href="/home" class="block text-center glass-card text-slate-200 py-3 rounded-xl font-bold border border-white/10">&larr; Back</a>
    </div>
    """
    return render_template_string(BASE_HTML, content=render_template_string(inner_content))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        u = request.form.get('username')
        ph = request.form.get('phone')
        if User.query.filter_by(username=u).first():
            error = "Username taken!"
        else:
            db.session.add(User(
                username=u, phone=ph, email=request.form.get('email'), 
                password=request.form.get('password'), ff_uid=request.form.get('ff_uid'), 
                wallet=0, winnings=0, role='user',
                profile_pic=f"https://api.dicebear.com/7.x/bottts/svg?seed={u}"
            ))
            db.session.commit()
            return redirect(url_for('login'))
    content = f"""
    <div class="glass-card border border-white/10 p-6 rounded-3xl shadow-2xl max-w-sm mx-auto text-xs">
        <h2 class="text-sm font-black text-red-500 uppercase mb-4">Register</h2>
        {f'<div class="bg-red-500/20 text-red-400 p-3 rounded-xl mb-3 font-bold">{error}</div>' if error else ''}
        <form method="POST" class="space-y-3">
            <input type="text" name="username" placeholder="Username" required class="w-full bg-black/80 border border-white/10 rounded-xl p-3 text-white">
            <input type="text" name="phone" placeholder="Phone" required class="w-full bg-black/80 border border-white/10 rounded-xl p-3 text-white">
            <input type="email" name="email" placeholder="Email" required class="w-full bg-black/80 border border-white/10 rounded-xl p-3 text-white">
            <input type="text" name="ff_uid" placeholder="Free Fire UID" required class="w-full bg-black/80 border border-white/10 rounded-xl p-3 text-white">
            <input type="password" name="password" placeholder="Password" required class="w-full bg-black/80 border border-white/10 rounded-xl p-3 text-white">
            <button type="submit" class="w-full bg-gradient-to-r from-red-600 to-rose-600 font-bold py-3.5 rounded-xl text-white shadow-lg glow-red">Register</button>
        </form>
        <p class="text-center text-slate-400 mt-4">Have account? <a href="/login" class="text-red-400 font-bold">Login</a></p>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username'), password=request.form.get('password')).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = "Invalid Login!"
    content = f"""
    <div class="glass-card border border-white/10 p-6 rounded-3xl shadow-2xl max-w-sm mx-auto text-xs">
        <h2 class="text-sm font-black text-red-500 uppercase mb-4">Login</h2>
        {f'<div class="bg-red-500/20 text-red-400 p-3 rounded-xl mb-3 font-bold">{error}</div>' if error else ''}
        <form method="POST" class="space-y-3.5">
            <input type="text" name="username" placeholder="Username" required class="w-full bg-black/80 border border-white/10 rounded-xl p-3.5 text-white">
            <input type="password" name="password" placeholder="Password" required class="w-full bg-black/80 border border-white/10 rounded-xl p-3.5 text-white">
            <button type="submit" class="w-full bg-gradient-to-r from-red-600 to-rose-600 font-bold py-3.5 rounded-xl text-white shadow-lg glow-red">Login</button>
        </form>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('splash'))

@app.route('/profile')
@login_required
def profile():
    content = f"""
    <div class="glass-card border border-white/10 p-6 rounded-2xl shadow-2xl text-xs space-y-4">
        <h2 class="text-sm font-black text-indigo-400 uppercase">👤 Profile</h2>
        <div class="flex flex-col items-center justify-center space-y-2.5 py-4 bg-black/60 rounded-xl">
            <img src="{current_user.profile_pic}" class="w-20 h-20 rounded-full border-2 border-indigo-500">
            <span class="font-black text-white text-sm">{current_user.username}</span>
        </div>
        <div class="bg-black/60 p-4 rounded-xl space-y-3">
            <p class="flex justify-between"><span class="text-slate-500">UID:</span> <span class="text-emerald-400 font-bold">{current_user.ff_uid}</span></p>
            <p class="flex justify-between"><span class="text-slate-500">Wallet:</span> <span class="text-yellow-400 font-black">₹{current_user.wallet}</span></p>
        </div>
        <a href="/home" class="block text-center glass-card text-slate-200 py-3 rounded-xl font-bold">&larr; Back</a>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route('/join/<int:match_id>', methods=['POST'])
@login_required
def join_match(match_id):
    match = Match.query.get_or_404(match_id)
    if not Registration.query.filter_by(user_id=current_user.id, match_id=match_id).first():
        if current_user.wallet >= match.entry_fee:
            current_user.wallet -= match.entry_fee
            db.session.add(Registration(user_id=current_user.id, match_id=match.id))
            db.session.commit()
        else:
            return redirect(url_for('wallet'))
    return redirect(url_for('games_section'))

@app.route('/host-panel', methods=['GET', 'POST'])
@login_required
def host_panel():
    if current_user.role not in ['admin', 'host']:
        return "Access Denied"
    if request.method == 'POST':
        match = Match.query.get_or_404(request.form.get('match_id'))
        match.room_id = request.form.get('room_id')
        match.room_pass = request.form.get('room_pass')
        match.winner_info = request.form.get('winner_info')
        db.session.commit()
        return redirect(url_for('host_panel'))
    matches = Match.query.all()
    inner_content = """
    <div class="glass-card border border-white/10 p-6 rounded-2xl shadow-2xl space-y-6 text-xs">
        <h2 class="text-sm font-black text-indigo-400 uppercase">⚡ Host Hub: Room & Results Manager</h2>
        <div class="space-y-4">
            {% for m in matches %}
            <form method="POST" class="bg-black/60 p-4 rounded-xl border border-white/5 space-y-3">
                <input type="hidden" name="match_id" value="{{ m.id }}">
                <div class="font-bold text-white text-sm">{{ m.title }}</div>
                <input type="text" name="room_id" value="{{ m.room_id }}" required class="w-full bg-black p-3 rounded-xl text-white font-mono">
                <input type="text" name="room_pass" value="{{ m.room_pass }}" required class="w-full bg-black p-3 rounded-xl text-white font-mono">
                <input type="text" name="winner_info" value="{{ m.winner_info }}" required class="w-full bg-black p-3 rounded-xl text-white font-mono" placeholder="Winner / Results Info">
                <button type="submit" class="w-full bg-indigo-600 font-bold py-3 rounded-xl text-white">Update Room & Results</button>
            </form>
            {% endfor %}
        </div>
        <a href="/home" class="block text-center glass-card text-slate-200 py-3 rounded-xl font-bold">&larr; Back</a>
    </div>
    """
    return render_template_string(BASE_HTML, content=render_template_string(inner_content, matches=matches))

@app.route('/admin-panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.role != 'admin':
        return "Access Denied"
    if request.method == 'POST':
        db.session.add(Match(
            title=request.form.get('title'),
            game_mode=request.form.get('game_mode'),
            map_name=request.form.get('map_name'),
            prize=request.form.get('prize'),
            entry_fee=int(request.form.get('entry_fee', 0)),
            room_id="Awaiting Room ID",
            room_pass="Awaiting Password",
            winner_info="Yet to be declared"
        ))
        db.session.commit()
        return redirect(url_for('admin_panel'))
    content = """
    <div class="glass-card border border-white/10 p-6 rounded-2xl shadow-2xl space-y-6 text-xs">
        <h2 class="text-sm font-black text-purple-400 uppercase">👑 Admin Tournament Creator</h2>
        <form method="POST" class="bg-black/60 p-4 rounded-xl space-y-3.5">
            <input type="text" name="title" placeholder="Title" required class="w-full bg-black p-3 rounded-xl text-white">
            <select name="game_mode" class="w-full bg-black p-3 rounded-xl text-white font-bold">
                <option value="CS 4v4">CS 4v4</option>
                <option value="CS 1v1">CS 1v1</option>
                <option value="BR">BR Full Map</option>
                <option value="Lone Wolf">Lone Wolf</option>
            </select>
            <input type="text" name="map_name" placeholder="Map" required class="w-full bg-black p-3 rounded-xl text-white">
            <input type="text" name="prize" placeholder="Prize" required class="w-full bg-black p-3 rounded-xl text-white">
            <input type="number" name="entry_fee" value="20" class="w-full bg-black p-3 rounded-xl text-white">
            <button type="submit" class="w-full bg-purple-600 font-bold py-3.5 rounded-xl text-white">Publish Match</button>
        </form>
        <a href="/home" class="block text-center glass-card text-slate-200 py-3 rounded-xl font-bold">&larr; Back</a>
    </div>
    """
    return render_template_string(BASE_HTML, content=content)

@app.route('/support')
def support():
    inner_content = """
    <div class="glass-card border border-white/10 p-6 rounded-2xl shadow-2xl text-xs space-y-4 text-center">
        <h2 class="text-sm font-black text-emerald-400 uppercase">🎧 24/7 Support Desk</h2>
        <p class="text-slate-400">WhatsApp Support:</p>
        <div class="bg-black/60 p-4 rounded-xl space-y-3">
            <span class="text-emerald-400 font-bold block text-sm font-mono">+91 82983 63286</span>
            <a href="https://wa.me/918298363286" target="_blank" class="inline-block bg-emerald-600 text-white font-bold px-5 py-2.5 rounded-xl">Chat on WhatsApp</a>
        </div>
        <a href="/home" class="block text-center glass-card text-slate-200 py-3 rounded-xl font-bold">&larr; Back</a>
    </div>
    """
    return render_template_string(BASE_HTML, content=render_template_string(inner_content))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

