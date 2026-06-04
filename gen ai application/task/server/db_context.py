"""Build a read-only text snapshot of movie_ticket_booking for the AI assistant."""


def build_database_context(cursor):
    sections = []

    cursor.execute("SELECT COUNT(*) FROM movie")
    movie_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM shows")
    show_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM booking")
    booking_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ticket")
    ticket_count = cursor.fetchone()[0]

    sections.append(
        "DATABASE: movie_ticket_booking\n"
        "TABLES: movie, shows, booking, ticket, users\n"
        f"ROW COUNTS: movie={movie_count}, shows={show_count}, "
        f"booking={booking_count}, ticket={ticket_count}, users={user_count}"
    )

    cursor.execute("""
        SELECT id, title, genre, duration, rating, description
        FROM movie
        ORDER BY title
    """)
    movies = cursor.fetchall()
    if movies:
        lines = ["MOVIES:"]
        for mid, title, genre, duration, rating, desc in movies:
            lines.append(
                f"- id {mid} | {title} | {genre} | {duration} min | "
                f"rating {rating} | {desc}"
            )
        sections.append("\n".join(lines))

    cursor.execute("""
        SELECT s.id, m.title, s.show_date, s.show_time, s.hall, s.price
        FROM shows s
        JOIN movie m ON s.movie_id = m.id
        ORDER BY s.show_date, s.show_time
    """)
    shows = cursor.fetchall()
    if shows:
        lines = ["SHOWS (showtimes):"]
        for sid, title, date, time, hall, price in shows:
            lines.append(
                f"- show #{sid} | {title} | {date} {time} | {hall} | ${price}"
            )
        sections.append("\n".join(lines))

    cursor.execute("""
        SELECT b.id, u.username, u.email, m.title, s.show_date, s.show_time,
               s.hall, b.booking_time, b.total_price
        FROM booking b
        JOIN users u ON b.user_id = u.id
        JOIN shows s ON b.show_id = s.id
        JOIN movie m ON s.movie_id = m.id
        ORDER BY b.booking_time DESC
    """)
    bookings = cursor.fetchall()
    if bookings:
        lines = ["BOOKINGS:"]
        for row in bookings:
            bid, user, email, title, date, time, hall, btime, total = row
            lines.append(
                f"- #{bid} {user} ({email}) | {title} | {date} {time} | "
                f"{hall} | ${total} | {btime}"
            )
        sections.append("\n".join(lines))

    cursor.execute("""
        SELECT t.id, t.seat_row, t.seat_num, b.id, m.title
        FROM ticket t
        JOIN booking b ON t.booking_id = b.id
        JOIN shows s ON b.show_id = s.id
        JOIN movie m ON s.movie_id = m.id
        ORDER BY t.id
    """)
    tickets = cursor.fetchall()
    if tickets:
        lines = ["TICKETS:"]
        for tid, row, num, bid, title in tickets:
            lines.append(
                f"- ticket #{tid} | booking #{bid} | {title} | "
                f"row {row} seat {num}"
            )
        sections.append("\n".join(lines))

    return "\n\n".join(sections)
