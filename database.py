import sqlite3

def init_db():
    """Создаёт таблицы в базе данных, если их нет"""
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS apps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category_id INTEGER,
        description TEXT,
        file_id TEXT,
        tutorial_text TEXT,
        tutorial_video TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    """)

    conn.commit()
    conn.close()

def get_categories():
    """Получает список категорий"""
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    conn.close()
    return categories

def get_apps_by_category(category_id):
    """Получает список приложений в категории"""
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM apps WHERE category_id = ?", (category_id,))
    apps = cur.fetchall()
    conn.close()
    return apps

def get_app_by_id(app_id):
    """Получает информацию о приложении по ID"""
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM apps WHERE id = ?", (app_id,))
    app = cur.fetchone()
    conn.close()
    return app