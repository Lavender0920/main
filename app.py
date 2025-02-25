from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

@app.route("/")
def home():
    authors = Author.query.all()
    return render_template("home.html", authors=authors)

@app.route("/author/<int:id>")
def read_author(id):
    author = Author.query.get_or_404(id)
    return render_template("read.html", author=author)

@app.route("/new", methods=["GET", "POST"])
def create_author():
    if request.method == "POST":
        name = request.form["name"]
        author = Author(name=name)
        db.session.add(author)
        db.session.commit()
        flash(f"Author {name} added successfully")
        return redirect(url_for("home"))
    return render_template("create.html")

@app.route("/author/<int:id>/book", methods=["GET", "POST"])
def create_book(id):
    author = Author.query.get_or_404(id)
    if request.method == "POST":
        title = request.form["title"]
        book = Book(title=title, author_id=author.id)
        db.session.add(book)
        db.session.commit()
        flash(f"Book '{title}' added to {author.name}")
        return redirect(url_for("read_author", id=author.id))
    return render_template("create_book.html", author=author)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def update_author(id):
    author = Author.query.get_or_404(id)
    if request.method == "POST":
        author.name = request.form["name"]
        db.session.commit()
        flash(f"Author {author.name} updated successfully")
        return redirect(url_for("home"))
    return render_template("update.html", author=author)

@app.route("/delete/<int:id>")
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    flash("Author deleted successfully")
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
