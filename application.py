from flask import Flask



app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.author} - {self.publisher}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'book_name': book.name, 'book_author': book.author, 'publisher': book.publisher}
        output.append(book_data)

    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"book_name": book.name, "book_author": book.author, "publisher": book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(name=request.jason['book_name'], author=request.jason['book_author'], publisher=request.jason['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}
