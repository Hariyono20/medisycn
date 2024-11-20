from flask import Flask, request, jsonify
from database import create_connection, create_table

app = Flask(__name__)


create_table()

@app.route('/api/register', methods=['POST'])
def register():
    
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

   
    if password != confirm_password:
        return jsonify({'error': 'Password and confirm password do not match.'}), 400

    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO users (name, email, phone, password)
        VALUES (%s, %s, %s, %s)
        """, (name, email, phone, password))
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({'message': 'User registered successfully!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
        SELECT * FROM users WHERE email = %s AND password = %s
        """, (email, password))

        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            return jsonify({'message': 'Login successful!', 'user': {'id': user[0], 'name': user[1], 'email': user[2]}}), 200
        else:
            return jsonify({'error': 'Invalid email or password.'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    create_table()
    app.run(debug=True)