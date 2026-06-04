import re

from config import MYSQL_DB
from database import get_db_connection
from db_context import build_database_context
from gemini import ask_gemini
from utils.security import is_restricted_request, get_restricted_response


class MovieChatbot:

    def _find_movie_title(self, cursor, msg):
        cursor.execute("SELECT title FROM movie")
        for (title,) in cursor.fetchall():
            if title and title.lower() in msg:
                return title
        return None

    def process_message(self, user_message):
        if not user_message or not user_message.strip():
            return "Please type a question about movies, shows, bookings, or tickets."

        if is_restricted_request(user_message):
            return get_restricted_response()

        msg = user_message.lower().strip()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # --- Database / schema ---
            if any(
                phrase in msg
                for phrase in [
                    "database",
                    "mysql",
                    "table",
                    "schema",
                    "how many",
                    "row count",
                    "columns",
                ]
            ):
                context = build_database_context(cursor)
                if "table" in msg or "schema" in msg or "column" in msg:
                    schema_info = (
                        "Tables in movie_ticket_booking:\n"
                        "• movie — id, title, description, genre, duration, rating, poster_path\n"
                        "• shows — id, movie_id, show_date, show_time, hall, price\n"
                        "• booking — id, user_id, show_id, booking_time, total_price\n"
                        "• ticket — id, booking_id, seat_row, seat_num\n"
                        "• users — id, username, email, role (passwords are not exposed)\n\n"
                    )
                    return schema_info + context
                return context

            if any(
                word in msg
                for word in ["coming soon", "upcoming", "releasing soon", "new movies"]
            ):
                cursor.execute("""
                    SELECT title, genre, description
                    FROM movie
                    ORDER BY title
                """)
                rows = cursor.fetchall()
                if not rows:
                    return "No movies in the database."
                response = (
                    "This database does not have a separate 'coming soon' flag. "
                    "All movies currently stored:\n\n"
                )
                for title, genre, desc in rows:
                    response += f"• {title} ({genre}) — {desc}\n"
                return response.strip()

            # --- Bookings ---
            if any(
                word in msg
                for word in ["booking", "bookings", "reservation", "reserved"]
            ):
                cursor.execute("""
                    SELECT b.id, u.username, u.email, m.title,
                           s.show_date, s.show_time, s.hall,
                           b.booking_time, b.total_price
                    FROM booking b
                    JOIN users u ON b.user_id = u.id
                    JOIN shows s ON b.show_id = s.id
                    JOIN movie m ON s.movie_id = m.id
                    ORDER BY b.booking_time DESC
                """)
                rows = cursor.fetchall()
                if not rows:
                    return "No bookings found."
                response = "Bookings:\n\n"
                for row in rows:
                    bid, user, email, title, date, time, hall, btime, total = row
                    response += (
                        f"#{bid} — {user} ({email})\n"
                        f"  {title} | {date} {time} | {hall}\n"
                        f"  ${total} | booked at {btime}\n\n"
                    )
                return response.strip()

            # --- Users (no passwords) ---
            if any(word in msg for word in ["user", "users", "customer", "admin"]):
                cursor.execute("""
                    SELECT id, username, email, role FROM users ORDER BY id
                """)
                rows = cursor.fetchall()
                if not rows:
                    return "No users found."
                response = "Users:\n\n"
                for uid, username, email, role in rows:
                    response += f"• #{uid} {username} ({email}) — role: {role}\n"
                return response.strip()

            # --- Tickets / seats (after price so "ticket prices" works) ---
            if any(word in msg for word in ["seat", "seats"]) or (
                "ticket" in msg
                and not any(w in msg for w in ["price", "cost", "fee", "how much"])
            ):
                cursor.execute("""
                    SELECT t.id, t.seat_row, t.seat_num, m.title,
                           s.show_date, s.show_time, s.hall
                    FROM ticket t
                    JOIN booking b ON t.booking_id = b.id
                    JOIN shows s ON b.show_id = s.id
                    JOIN movie m ON s.movie_id = m.id
                    ORDER BY t.id
                """)
                rows = cursor.fetchall()
                if not rows:
                    return "No tickets found in the database."
                response = "Tickets:\n\n"
                for tid, row, num, title, date, time, hall in rows:
                    response += (
                        f"• Ticket #{tid} — {title}\n"
                        f"  {date} {time} | {hall} | Row {row}, Seat {num}\n\n"
                    )
                return response.strip()

            # --- Price ---
            if any(
                word in msg
                for word in ["price", "cost", "fee", "how much"]
            ):
                cursor.execute("""
                    SELECT m.title, s.show_date, s.show_time, s.hall, s.price
                    FROM shows s
                    JOIN movie m ON s.movie_id = m.id
                    ORDER BY s.show_date, s.show_time
                """)
                rows = cursor.fetchall()
                if not rows:
                    return "No show prices found."
                response = "Show prices:\n\n"
                for title, date, time, hall, price in rows:
                    response += (
                        f"• {title} — {date} {time} | {hall} | ${price}\n"
                    )
                return response.strip()

            # --- Genre ---
            genre_match = re.search(
                r"(genre|type of movie|movies in)\s+([a-z\-]+)", msg
            )
            genres = [
                "sci-fi", "action", "thriller", "comedy", "horror", "drama", "romance"
            ]
            genre = genre_match.group(2) if genre_match else None
            if not genre:
                genre = next((g for g in genres if g in msg), None)
            if genre or "genre" in msg:
                if genre:
                    cursor.execute("""
                        SELECT title, rating, duration, description
                        FROM movie
                        WHERE LOWER(genre) LIKE %s
                        ORDER BY title
                    """, (f"%{genre}%",))
                    rows = cursor.fetchall()
                    if not rows:
                        return f"No movies found for genre '{genre}'."
                    response = f"Movies in genre '{genre}':\n\n"
                    for title, rating, duration, desc in rows:
                        response += (
                            f"• {title} — rating {rating}, {duration} min\n"
                            f"  {desc}\n\n"
                        )
                    return response.strip()

            # --- List movies (before showtimes; avoid matching bare "show") ---
            if any(
                phrase in msg
                for phrase in [
                    "now showing",
                    "available movies",
                    "list movies",
                    "show movies",
                    "all movies",
                    "what movies",
                ]
            ) or msg in ("movies", "movie"):
                cursor.execute("""
                    SELECT title, genre, duration, rating, description
                    FROM movie
                    ORDER BY title
                """)
                rows = cursor.fetchall()
                if not rows:
                    return "No movies in the database."
                response = "Movies:\n\n"
                for title, genre, duration, rating, desc in rows:
                    response += (
                        f"• {title} ({genre}) — rating {rating}, {duration} min\n"
                        f"  {desc}\n\n"
                    )
                return response.strip()

            # --- Showtimes / halls ---
            if any(
                word in msg
                for word in [
                    "showtime",
                    "showtimes",
                    "timing",
                    "show time",
                    "schedule",
                    "when is",
                    "hall",
                    "screen",
                ]
            ):
                title_filter = self._find_movie_title(cursor, msg)
                if title_filter:
                    cursor.execute("""
                        SELECT m.title, s.show_date, s.show_time, s.hall, s.price
                        FROM shows s
                        JOIN movie m ON s.movie_id = m.id
                        WHERE m.title = %s
                        ORDER BY s.show_date, s.show_time
                    """, (title_filter,))
                else:
                    cursor.execute("""
                        SELECT m.title, s.show_date, s.show_time, s.hall, s.price
                        FROM shows s
                        JOIN movie m ON s.movie_id = m.id
                        ORDER BY s.show_date, s.show_time
                    """)
                rows = cursor.fetchall()
                if not rows:
                    return "No shows scheduled."
                response = "Show schedule:\n\n"
                for title, date, time, hall, price in rows:
                    response += (
                        f"• {title}\n"
                        f"  {date} {time} | {hall} | ${price}\n\n"
                    )
                return response.strip()

            # --- Halls / theaters ---
            if any(
                word in msg
                for word in ["theater", "theatre", "cinema", "multiplex", "hall"]
            ):
                cursor.execute("""
                    SELECT DISTINCT s.hall FROM shows s ORDER BY s.hall
                """)
                halls = [r[0] for r in cursor.fetchall()]
                if not halls:
                    return "No halls found."
                response = "Halls / screens:\n\n"
                for hall in halls:
                    cursor.execute("""
                        SELECT m.title, s.show_date, s.show_time, s.price
                        FROM shows s
                        JOIN movie m ON s.movie_id = m.id
                        WHERE s.hall = %s
                        ORDER BY s.show_date, s.show_time
                    """, (hall,))
                    shows = cursor.fetchall()
                    response += f"• {hall}\n"
                    for title, date, time, price in shows:
                        response += f"    - {title} | {date} {time} | ${price}\n"
                    response += "\n"
                return response.strip()

            # --- Movie details ---
            movie_title = self._find_movie_title(cursor, msg)
            if movie_title and any(
                w in msg
                for w in ["about", "tell", "info", "detail", "describe", "what is"]
            ):
                cursor.execute("""
                    SELECT title, genre, duration, rating, description
                    FROM movie WHERE title = %s
                """, (movie_title,))
                row = cursor.fetchone()
                if row:
                    title, genre, duration, rating, desc = row
                    cursor.execute("""
                        SELECT show_date, show_time, hall, price
                        FROM shows s
                        JOIN movie m ON s.movie_id = m.id
                        WHERE m.title = %s
                        ORDER BY show_date, show_time
                    """, (movie_title,))
                    shows = cursor.fetchall()
                    response = (
                        f"{title}\n"
                        f"Genre: {genre} | Rating: {rating} | Duration: {duration} min\n\n"
                        f"{desc}\n"
                    )
                    if shows:
                        response += "\nShows:\n"
                        for date, time, hall, price in shows:
                            response += f"• {date} {time} | {hall} | ${price}\n"
                    return response.strip()

            db_context = build_database_context(cursor)
            return ask_gemini(f"""You are a Movie Ticket Booking assistant connected to MySQL database movie_ticket_booking.

RULES:
- Answer ONLY using the LIVE DATABASE DATA below.
- Tables: movie, shows, booking, ticket, users. Never expose password_hash.
- Do NOT invent movies, shows, or prices.
- READ-ONLY: do not help add, update, delete, or book tickets.
- If unrelated, politely refuse.
- Be concise; use bullet points for lists.

LIVE DATABASE DATA:
{db_context}

USER QUESTION:
{user_message}
""")

        except Exception as e:
            return (
                f"Database error: {e}\n\n"
                f"App is configured for database: {MYSQL_DB}\n"
                "Fix: set MYSQL_DB=movie_ticket_booking in task/.env, "
                "restart the server, and remove any old MYSQL_DB "
                "environment variable (e.g. movie_booking_db)."
            )

        finally:
            cursor.close()
            conn.close()
