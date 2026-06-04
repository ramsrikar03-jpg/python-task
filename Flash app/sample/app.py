from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'cinema_secret_key_123' # Change this to something secure

# Paths to JSON database files
USERS_FILE = os.path.join('data', 'users.json')
BOOKINGS_FILE = os.path.join('data', 'bookings.json')

# Ensure data directory and files exist
os.makedirs('data', exist_ok=True)
for file in [USERS_FILE, BOOKINGS_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)

# Mock Data for Movies and Showtimes
MOVIES = {
    "1": {
        "title": "Interstellar",
        "genre": "Sci-Fi / Drama",
        "banner": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=800",
        "timings": ["12:00 PM", "03:30 PM", "07:00 PM", "10:30 PM"],
        "price": 12.50
    },
    "2": {
        "title": "The Dark Knight",
        "genre": "Action / Thriller",
        "banner": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800",
        "timings": ["01:00 PM", "04:30 PM", "08:00 PM"],
        "price": 14.00
    },
    "3": {
        "title": "Inception",
        "genre": "Sci-Fi / Action",
        "banner": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=800",
        "timings": ["11:00 AM", "02:30 PM", "06:00 PM", "09:30 PM"],
        "price": 11.00
    }
}

# Helper functions to read/write JSON
def read_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def write_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

# --- ROUTES ---

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('movies'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = read_json(USERS_FILE)
        if any(u['username'] == username for u in users):
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))
        
        users.append({'username': username, 'password': password})
        write_json(USERS_FILE, users)
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        users = read_json(USERS_FILE)
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        
        if user:
            session['user'] = username
            return redirect(url_for('movies'))
        else:
            flash('Invalid username or password!', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/movies')
def movies():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('movies.html', movies=MOVIES)

@app.route('/select-seats/<movie_id>')
def select_seats(movie_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    timing = request.args.get('timing')
    if not timing:
        flash('Please select a showtime first!', 'error')
        return redirect(url_for('movies'))
        
    movie = MOVIES.get(movie_id)
    
    # Find already booked seats for this specific movie and time
    bookings = read_json(BOOKINGS_FILE)
    booked_seats = []
    for b in bookings:
        if b['movie_id'] == movie_id and b['timing'] == timing:
            booked_seats.extend(b['seats'])
            
    return render_template('seats.html', movie_id=movie_id, movie=movie, timing=timing, booked_seats=booked_seats)

@app.route('/book', methods=['POST'])
def book():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    movie_id = request.form.get('movie_id')
    timing = request.form.get('timing')
    selected_seats = request.form.getlist('seats')
    
    if not selected_seats:
        flash('Please select at least one seat!', 'error')
        return redirect(url_for('select_seats', movie_id=movie_id, timing=timing))
        
    movie = MOVIES.get(movie_id)
    total_price = len(selected_seats) * movie['price']
    
    # Save booking into JSON
    bookings = read_json(BOOKINGS_FILE)
    new_booking = {
        "booking_id": len(bookings) + 1,
        "username": session['user'],
        "movie_id": movie_id,
        "movie_title": movie['title'],
        "timing": timing,
        "seats": selected_seats,
        "total_price": total_price
    }
    bookings.append(new_booking)
    write_json(BOOKINGS_FILE, bookings)
    
    return render_template('confirmation.html', booking=new_booking)

if __name__ == '__main__':
    app.run(debug=True)