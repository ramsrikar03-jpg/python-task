import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import app, db, User, Movie, Show, Booking, Ticket, seed_data, ensure_mysql_database
from werkzeug.security import check_password_hash


def run_tests():
    print("Starting Flask Movie Booking Application Verification...")

    ensure_mysql_database()

    with app.app_context():
        print("Recreating database tables...")
        db.create_all()
        seed_data()

        print("Checking seeded users...")
        admin = User.query.filter_by(username='admin').first()
        customer = User.query.filter_by(username='john_doe').first()

        if admin:
            print(f"Found Admin User: {admin.username} ({admin.email})")
            assert admin.role == 'admin', "Admin role mismatch!"
            assert check_password_hash(admin.password_hash, 'admin123'), "Admin password verification failed!"
        else:
            print("ERROR: Admin user not seeded!")
            sys.exit(1)

        if customer:
            print(f"Found Customer User: {customer.username} ({customer.email})")
            assert customer.role == 'customer', "Customer role mismatch!"
            assert check_password_hash(customer.password_hash, 'customer123'), "Customer password verification failed!"
        else:
            print("ERROR: Customer user not seeded!")
            sys.exit(1)

        print("Checking seeded movies...")
        movies = Movie.query.all()
        print(f"Total seeded movies: {len(movies)}")
        for m in movies:
            print(f" - [{m.id}] {m.title} ({m.genre}), Duration: {m.duration}m, Rating: {m.rating}")
            assert m.poster_path in [
                'poster_interstellar.png',
                'poster_cyberpunk.png',
                'poster_thriller.png',
            ], f"Unexpected poster path: {m.poster_path}"

        print("Checking seeded showtimes...")
        shows = Show.query.all()
        print(f"Total seeded shows: {len(shows)}")
        for s in shows:
            print(
                f" - [{s.id}] Movie: {s.movie.title}, Hall: {s.hall}, "
                f"Time: {s.show_date} @ {s.show_time}, Price: ${s.price}"
            )
            assert s.price > 0, "Show price must be positive!"

        print("Simulating a seat booking...")
        Booking.query.filter_by(user_id=customer.id).delete()
        db.session.commit()

        test_show = Show.query.first()
        assert test_show is not None, "No shows found to perform test booking!"

        seats_to_book = [('A', 5), ('A', 6)]
        total_price = len(seats_to_book) * test_show.price

        new_booking = Booking(
            user_id=customer.id,
            show_id=test_show.id,
            total_price=total_price
        )
        db.session.add(new_booking)
        db.session.flush()

        for r, n in seats_to_book:
            db.session.add(Ticket(booking_id=new_booking.id, seat_row=r, seat_num=n))

        db.session.commit()
        print(
            f"Successfully booked seats A5 and A6 for '{test_show.movie.title}' "
            f"(Total: ${total_price})!"
        )

        bookings = Booking.query.filter_by(user_id=customer.id).all()
        assert len(bookings) == 1, "Expected exactly 1 booking!"
        assert len(bookings[0].tickets) == 2, "Expected exactly 2 tickets in booking!"
        booked_seat_labels = [f"{t.seat_row}{t.seat_num}" for t in bookings[0].tickets]
        print(f"Verified tickets in DB: {', '.join(booked_seat_labels)}")

        db.session.delete(bookings[0])
        db.session.commit()
        print("Verification complete: All models, relationships, and seed data operate perfectly!")


if __name__ == '__main__':
    run_tests()
