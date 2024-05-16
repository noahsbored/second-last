from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
import mysql.connector 
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)


def db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Noach-123",
            database="books1"
        )
        print("connected")
        return conn
    except mysql.connector.Error as e:
        print(e)
        return None


class BookSchema(ma.Schema):
    class Meta:
        fields = ('title', 'isbn', 'publication_date')

book_schema = BookSchema()


@app.route('/books', methods=['POST'])
def add_book():
    try:
        
        book_data = request.json
        
      
        conn = db_connection()
        if conn is not None:
            cursor = conn.cursor()

       
            query = "INSERT INTO books (title, isbn, publication_date) VALUES (%s, %s, %s)"
            cursor.execute(query, (book_data['title'], book_data['isbn'], book_data['publication_date']))
            conn.commit()

           
            cursor.close()
            conn.close()

            return jsonify({'message': 'sucsess'}), 201
        else:
            return jsonify({'error': 'failed'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
