from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

app = Flask(__name__)


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db.init_app(app)


class Book(db.Model):
    __tablename__ = 'List of Books'
    id = db.Column(Integer, primary_key=True, unique=True)
    title = db.Column(String(150), unique=True, nullable=False)
    author = db.Column(String(150), nullable=False)
    rating = db.Column(String, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.execute(db.select(Book).order_by(Book.title)).scalars()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        db.session.add(Book(title=title, author=author, rating=rating))
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        id_ = request.form["id"]
        changed_rating = request.form["edited_rating"]
        book_to_update = db.get_or_404(Book, id_)
        book_to_update.rating = str(changed_rating)
        db.session.commit()
        return redirect(url_for("home"))
    id_ = request.args.get("id")
    book = db.get_or_404(Book, id_)
    return render_template("edit.html", book=book)


@app.route("/delete")
def delete():
    book = request.args.get("id_")
    to_delete = db.get_or_404(Book, book)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

