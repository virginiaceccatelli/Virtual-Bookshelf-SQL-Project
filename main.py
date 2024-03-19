from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)


class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db.init_app(app)


class Book(db.Model):
    __tablename__ = 'List of Books'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    title: Mapped[String] = mapped_column(String(150), unique=True, nullable=False)
    author: Mapped[String] = mapped_column(String(150), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html", books=db.session.query(Book).all())


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


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id_):
    if request.method == "GET":
        changed_rating = request.form["changed rating"]
        book_to_update = db.get_or_404(Book, id_)
        book_to_update.rating = changed_rating
        db.session.commit()
        return render_template("edit.html")


if __name__ == "__main__":
    app.run(debug=True)

