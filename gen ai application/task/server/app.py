from flask import Flask

from config import MYSQL_DB
from database import get_db_connection
from routes.chatbot_routes import chatbot_bp
from routes.main_routes import main_bp

app = Flask(
    __name__,
    template_folder="../client/templates",
    static_folder="../client/static",
)

app.register_blueprint(main_bp)
app.register_blueprint(chatbot_bp)


def _verify_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DATABASE()")
        active_db = cursor.fetchone()[0]
        cursor.execute("SHOW TABLES LIKE 'movie'")
        if not cursor.fetchone():
            raise RuntimeError(
                f"Table 'movie' not found in '{active_db}'. "
                "Use database movie_ticket_booking in MySQL Workbench."
            )
        print(f"MySQL connected: database={active_db}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print(f"Using MYSQL_DB={MYSQL_DB} (from task/.env)")
    try:
        _verify_database()
    except Exception as exc:
        print(f"Database check failed: {exc}")
    app.run(debug=True)
