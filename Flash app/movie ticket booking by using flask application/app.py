import os
import urllib.parse
from datetime import datetime, date

import pymysql
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# =========================
# FLASK APP CONFIGURATION
# =========================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def load_env_file():
    """Load MYSQL_* variables from a .env file in the project folder."""
    env_path = os.path.join(BASE_DIR, '.env')
    if not os.path.isfile(env_path):
        return
    with open(env_path, encoding='utf-8') as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


load_env_file()

MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_HOST = os.environ.get('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
MYSQL_DATABASE = os.environ.get(
    'MYSQL_DATABASE',
    os.environ.get('MYSQL_DB', 'movie_ticket_booking'),
)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.config['SECRET_KEY'] = 'movie_ticket_secret_key_12345'
_password = urllib.parse.quote_plus(MYSQL_PASSWORD)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'mysql+pymysql://{MYSQL_USER}:{_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    '?charset=utf8mb4'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}

print("BASE DIRECTORY :", BASE_DIR)
print("TEMPLATE PATH  :", app.template_folder)
print("STATIC PATH    :", app.static_folder)

db = SQLAlchemy(app)

# =========================
# DATABASE MODELS
# =========================

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='customer')

    bookings = db.relationship('Booking', backref='user', lazy=True)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    poster_path = db.Column(db.String(200), nullable=False)

    shows = db.relationship(
        'Show',
        backref='movie',
        cascade="all, delete-orphan",
        lazy=True
    )


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movie.id'),
        nullable=False
    )

    show_date = db.Column(db.String(50), nullable=False)
    show_time = db.Column(db.String(50), nullable=False)
    hall = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    bookings = db.relationship(
        'Booking',
        backref='show',
        cascade="all, delete-orphan",
        lazy=True
    )


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    show_id = db.Column(
        db.Integer,
        db.ForeignKey('shows.id'),
        nullable=False
    )

    booking_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    total_price = db.Column(db.Float, nullable=False)

    tickets = db.relationship(
        'Ticket',
        backref='booking',
        cascade="all, delete-orphan",
        lazy=True
    )


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey('booking.id'),
        nullable=False
    )

    seat_row = db.Column(db.String(5), nullable=False)
    seat_num = db.Column(db.Integer, nullable=False)


# =========================
# SEED DATA
# =========================

def seed_data():

    admin_user = User.query.filter_by(username='admin').first()

    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@cinema.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )

        db.session.add(admin_user)

    if not User.query.filter_by(username='john_doe').first():
        db.session.add(
            User(
                username='john_doe',
                email='john@example.com',
                password_hash=generate_password_hash('customer123'),
                role='customer'
            )
        )

    if Movie.query.count() == 0:

        movie1 = Movie(
            title="Interstellar Odyssey",
            description="Epic Sci-Fi adventure movie.",
            genre="Sci-Fi",
            duration=169,
            rating=8.6,
            poster_path="poster_interstellar.png"
        )

        movie2 = Movie(
            title="Cyberpunk 2099",
            description="Futuristic action thriller.",
            genre="Action",
            duration=124,
            rating=7.9,
            poster_path="poster_cyberpunk.png"
        )

        movie3 = Movie(
            title="The Whispering Shadows",
            description="Mystery thriller movie.",
            genre="Thriller",
            duration=142,
            rating=8.2,
            poster_path="poster_thriller.png"
        )

        db.session.add_all([movie1, movie2, movie3])
        db.session.commit()

        today = date.today().strftime('%Y-%m-%d')

        shows = [
            Show(movie_id=movie1.id, show_date=today, show_time="14:00", hall="Screen 1", price=12.5),
            Show(movie_id=movie1.id, show_date=today, show_time="18:30", hall="Screen 1", price=14.0),
            Show(movie_id=movie2.id, show_date=today, show_time="16:00", hall="Screen 2", price=10.5),
            Show(movie_id=movie3.id, show_date=today, show_time="19:30", hall="Screen 3", price=13.5),
        ]

        db.session.add_all(shows)

    db.session.commit()


# =========================
# CONTEXT PROCESSOR
# =========================

@app.context_processor
def inject_user():

    user = None

    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])

    return dict(current_user=user)


# =========================
# ROUTES
# =========================

@app.route('/')
def home():

    print("Loading templates from :", app.template_folder)

    movies = Movie.query.all()

    return render_template('index.html', movies=movies)


@app.route('/test')
def test():
    return "Flask Working Perfectly"


@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):

    movie = Movie.query.get_or_404(movie_id)

    shows = Show.query.filter_by(movie_id=movie.id).all()

    return render_template(
        'movie_detail.html',
        movie=movie,
        shows=shows
    )


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):

            session['user_id'] = user.id
            session['role'] = user.role

            flash('Successfully logged in!', 'success')

            return redirect(url_for('home'))

        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():

    session.clear()

    flash('Logged out successfully!', 'info')

    return redirect(url_for('home'))


@app.route('/book/<int:show_id>')
def book_seats(show_id):
    if 'user_id' not in session:
        flash('Please log in to book tickets.', 'warning')
        return redirect(url_for('login'))
    
    show = Show.query.get_or_404(show_id)
    # Fetch all booked tickets for this show
    booked_tickets = Ticket.query.join(Booking).filter(Booking.show_id == show_id).all()
    # List of "Row-Num" strings representing booked seats
    booked_seat_labels = [f"{t.seat_row}-{t.seat_num}" for t in booked_tickets]
    
    # 8 Rows (A-H), 10 Columns (1-10)
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cols = list(range(1, 11))
    
    return render_template('book_seats.html', show=show, rows=rows, cols=cols, booked_seats=booked_seat_labels)


@app.route('/api/book', methods=['POST'])
def api_book():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        
    data = request.get_json()
    show_id = data.get('show_id')
    selected_seats = data.get('seats', [])
    
    if not selected_seats:
        return jsonify({'success': False, 'message': 'No seats selected'}), 400
        
    show = Show.query.get(show_id)
    if not show:
        return jsonify({'success': False, 'message': 'Show not found'}), 404
        
    # Double check if any selected seat is already booked
    for seat in selected_seats:
        row, num = seat.split('-')
        num = int(num)
        exists = Ticket.query.join(Booking).filter(
            Booking.show_id == show_id,
            Ticket.seat_row == row,
            Ticket.seat_num == num
        ).first()
        if exists:
            return jsonify({'success': False, 'message': f'Seat {row}{num} is already booked.'}), 400

    # Create Booking
    total_price = len(selected_seats) * show.price
    new_booking = Booking(
        user_id=session['user_id'],
        show_id=show_id,
        total_price=total_price
    )
    db.session.add(new_booking)
    db.session.flush()

    # Create Tickets
    for seat in selected_seats:
        row, num = seat.split('-')
        num = int(num)
        new_ticket = Ticket(booking_id=new_booking.id, seat_row=row, seat_num=num)
        db.session.add(new_ticket)
        
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Booking successful!',
        'booking_id': new_booking.id
    })


@app.route('/booking/<int:booking_id>')
def booking_confirmation(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != session['user_id'] and session.get('role') != 'admin':
        flash('Unauthorized access to booking.', 'danger')
        return redirect(url_for('home'))
    
    return render_template('booking_confirmation.html', booking=booking)


@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_bookings = Booking.query.filter_by(user_id=session['user_id']).order_by(Booking.booking_time.desc()).all()
    return render_template('booking_history.html', bookings=user_bookings)


@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Admin authorization required.', 'danger')
        return redirect(url_for('home'))
    
    movies = Movie.query.all()
    bookings = Booking.query.order_by(Booking.booking_time.desc()).all()
    return render_template('admin.html', movies=movies, bookings=bookings)


@app.route('/admin/movie/add', methods=['POST'])
def admin_add_movie():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    
    title = request.form['title']
    description = request.form['description']
    genre = request.form['genre']
    duration = int(request.form['duration'])
    rating = float(request.form['rating'])
    poster_path = request.form.get('poster_path', 'default_poster.png')
    
    new_movie = Movie(
        title=title,
        description=description,
        genre=genre,
        duration=duration,
        rating=rating,
        poster_path=poster_path
    )
    db.session.add(new_movie)
    db.session.commit()
    flash('Movie added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/movie/delete/<int:movie_id>', methods=['POST'])
def admin_delete_movie(movie_id):
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/show/add', methods=['POST'])
def admin_add_show():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    
    movie_id = int(request.form['movie_id'])
    show_date = request.form['show_date']
    show_time = request.form['show_time']
    hall = request.form['hall']
    price = float(request.form['price'])
    
    new_show = Show(
        movie_id=movie_id,
        show_date=show_date,
        show_time=show_time,
        hall=hall,
        price=price
    )
    db.session.add(new_show)
    db.session.commit()
    flash('Showtime added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/show/delete/<int:show_id>', methods=['POST'])
def admin_delete_show(show_id):
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    
    show = Show.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    flash('Showtime deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


# =========================
# MYSQL SETUP
# =========================

def ensure_mysql_database():
    """Create movie_ticket_booking database if it does not exist."""
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        port=int(MYSQL_PORT),
        charset='utf8mb4',
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.commit()
    finally:
        connection.close()


# =========================
# MAIN
# =========================

if __name__ == '__main__':

    try:
        ensure_mysql_database()
    except pymysql.Error as exc:
        print(
            "Could not connect to MySQL. Start MySQL Server, set MYSQL_USER / "
            f"MYSQL_PASSWORD if needed, then run database_setup.sql in Workbench.\nError: {exc}"
        )
        raise SystemExit(1) from exc

    with app.app_context():
        db.create_all()
        seed_data()

    app.run(debug=True)