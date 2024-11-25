from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import create_connection, create_table
import re

app = Flask(__name__)

# Membuat tabel jika belum ada
create_table()

# Fungsi untuk validasi email
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    # Validasi input
    if not all([name, email, password, confirm_password]):
        return jsonify({'error': 'All fields are required'}), 400
    
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Password and confirm password do not match.'}), 400

    # Hashing password sebelum menyimpannya ke database
    hashed_password = generate_password_hash(password)

    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Menyimpan data pengguna ke database tanpa kolom phone
        cursor.execute("""
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        """, (name, email, hashed_password))
        
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'User registered successfully!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Menangani jika ada error dalam blok try

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Validasi input, pastikan email dan password ada
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Mencari user berdasarkan email
        cursor.execute("""
        SELECT * FROM users WHERE email = %s
        """, (email,))

        user = cursor.fetchone()  # Mengambil satu baris data user
        cursor.close()
        connection.close()

        # Mengecek apakah user ditemukan dan password yang diberikan cocok
        if user:
            # Pastikan ada 5 kolom yang diambil (id, name, email, password, dan kolom lainnya jika ada)
            if len(user) >= 4:
                # Verifikasi password menggunakan check_password_hash
                if check_password_hash(user[3], password):  # user[3] adalah password yang di-hash
                    return jsonify({'message': 'Login successful!', 'user': {'id': user[0], 'name': user[1], 'email': user[2]}}), 200
                else:
                    return jsonify({'error': 'Invalid email or password.'}), 401
            else:
                return jsonify({'error': 'Invalid email or password.'}), 401
        else:
            return jsonify({'error': 'Invalid email or password.'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
