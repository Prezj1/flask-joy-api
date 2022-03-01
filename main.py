import re
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
from sqlalchemy import delete
from comic_books import books, message, no_book, book_deleted
from flask_cors import CORS
from http import HTTPStatus

app = Flask(__name__)
api = Api(app)
CORS(app)

class Books(Resource):
    def get(self):
        return make_response(jsonify(books))


class New(Resource):
    def post(self):
        data = request.get_json("https://flask-joy-api.herokuapp.com/")
        title = data.get('book_title')
        author = data.get('book_author')
        publisher = data.get('publisher')
        description = data.get('description')
        book = {
            "id": len(books)+1,  
            "title": title,
            "author": author,
            "publisher": publisher,
            "description": description
            }
        books.append(book)
        return make_response(jsonify(books), HTTPStatus.CREATED)


class Update(Resource):
    def put(self,book_id):
        book = next((book for book in books if book['id'] == book_id),None) 
        if not book:
            return make_response(jsonify(message),HTTPStatus.NOT_FOUND)
        data = request.get_json("https://flask-joy-api.herokuapp.com/")
        book.update(
        {
            'title': data.get('book_title'),
            'author': data.get('book_author'),
            'publisher': data.get('publisher'),
            'description': data.get('description'),
            }
        )
        return make_response(jsonify(book))


class Book(Resource):
    def get(self, book_id):
        book = next(
            (book for book in books if book['id'] ==book_id),None) 
        if book:
            return jsonify(book)
        return make_response(jsonify(message),HTTPStatus.NOT_FOUND)

    def delete(self, book_id):
        for book in books:
            if book['id'] == book_id:
                del book
                return make_response(jsonify(book_deleted))
            return make_response(jsonify(no_book),HTTPStatus.NOT_FOUND)

        



api.add_resource(Books, '/')
api.add_resource(Book, '//<int:book_id>')
api.add_resource(Update, '//<int:book_id>')
api.add_resource(New, '/')

if __name__ == '__main__':
    app.run(debug=True)