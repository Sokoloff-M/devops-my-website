import os
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Подключаемся к базе данных по имени сервиса "db"
        conn = psycopg2.connect(
            host="db",
            database=os.environ.get("POSTGRES_DB", "mydatabase"),
            user=os.environ.get("POSTGRES_USER", "myuser"),
            password=os.environ.get("POSTGRES_PASSWORD", "mysecretpassword")
        )
        cur = conn.cursor()
        cur.execute("SELECT name FROM users;")
        rows = cur.fetchall()
        
        # Формируем ответ
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"<h1>Docker + Postgres</h1>")
        self.wfile.write(b"<ul>")
        for row in rows:
            self.wfile.write(f"<li>{row[0]}</li>".encode('utf-8'))
        self.wfile.write(b"</ul>")

HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
