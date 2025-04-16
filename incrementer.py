import os 
from flask import Flask, render_template_string, request, redirect, url_for
from flask_socketio import SocketIO
from dotenv import load_dotenv
from supabase import create_client, Client
from main import create_lpdf

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5000")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def increment_count():
    response = supabase.table("test").select("count").limit(1).execute()
    data = response.data
    if data and len(data) > 0:
        current_count = data[0]["count"]
        new_count = current_count + 1
        supabase.table("test").update({"count": new_count}).eq("id", 1).execute()
        return new_count
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_count = increment_count()
        
        create_lpdf(f"demo.lpdf")
        print('[Incrementer] PDF created. Emitting pdf_updated event.')
        socketio.emit('pdf_updated')
        return redirect(url_for("index"))
    html = """
    <html>
    <head>
    <title>LPDF Incrementer</title>
    </head>
    <body>
    <h1>LPDF Incrementer</h1>
    <p>Click the button to increment the count and regenerate the LPDF</p>
    <form method="post">
    <button type="submit">Increment</button>
    </form>
    <p>After increment, <a href="http://localhost:5000/lpdf" target="_blank">view the LPDF</a>.</p>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    # Use socketio.run for proper WebSocket handling
    socketio.run(app, port=5001)