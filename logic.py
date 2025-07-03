# logic.py
import sqlite3
from datetime import datetime
from config import DATABASE, client

class CareerBotDB:
    def __init__(self, db_path=DATABASE):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    age INTEGER,
                    interests TEXT
                )
            ''')

            conn.execute('''
                CREATE TABLE IF NOT EXISTS liked_careers (
                    user_id INTEGER,
                    career_title TEXT,
                    liked_at TEXT,
                    ai_text TEXT
                )
            ''')

            conn.commit()

    def save_liked_career(self, user_id, title, ai_text):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO liked_careers (user_id, career_title, liked_at, ai_text) VALUES (?, ?, ?, ?)",
                (user_id, title, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ai_text)
            )
            conn.commit()

    def add_user(self, user_id, username, age, interests):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                'INSERT OR REPLACE INTO users (user_id, username, age, interests) VALUES (?, ?, ?, ?)',
                (user_id, username, age, interests)
            )
            conn.commit()

    def get_user_profile(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT username, age, interests FROM users WHERE user_id = ?", (user_id,))
            return cur.fetchone()

    def update_user(self, user_id, age, interests):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE users SET age = ?, interests = ? WHERE user_id = ?",
                (age, interests, user_id)
            )
            conn.commit()

    def delete_user(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()

    def generate_detailed_ai_suggestions(self, interests, username):
        prompt = (
            f"Kullanıcının adı: {username}\n"
            f"İlgi alanları: {interests}\n\n"
            "Bu kişi için kariyer önerileri hazırlamanı istiyorum. Kısa metinlerle 1 tane bilindik kariyer fikri öner.\n"
            "- Her öneri **başlık + açıklama + neden uygun olabilir?** formatında olmalı.\n"
            "- Sonuçları markdown formatında ver (başlıklar bold, listeler vs. kullanabilirsin).\n"
        )
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print("Gemini API hatası:", e)
            return None

    def get_liked_careers(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT career_title, liked_at, ai_text FROM liked_careers WHERE user_id = ? ORDER BY liked_at DESC",
                (user_id,)
            )
            return cur.fetchall()

if __name__ == "__main__":
    db = CareerBotDB()
    print("Veritabanı hazır.")