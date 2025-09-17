import os
from flask import Flask, Blueprint, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Profile, Author, Book, Student, Course

# -------------------- CONFIG --------------------
app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# -------------------- ERROR HANDLER --------------------
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# -------------------- SITEMAP --------------------
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# -------------------- BLUEPRINT --------------------
bp = Blueprint("api", __name__, url_prefix="/api")

# -------------------- USERS --------------------
@bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(username=data["username"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username})

@bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username} for u in users])

@bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "username": user.username})

@bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get("username", user.username)
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username})

@bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {user_id} deleted"})

# -------------------- PROFILES --------------------
@bp.route("/profiles", methods=["POST"])
def create_profile():
    data = request.json
    profile = Profile(bio=data["bio"], user_id=data["user_id"])
    db.session.add(profile)
    db.session.commit()
    return jsonify({"id": profile.id, "bio": profile.bio})

@bp.route("/profiles", methods=["GET"])
def get_profiles():
    profiles = Profile.query.all()
    return jsonify([{"id": p.id, "bio": p.bio, "user_id": p.user_id} for p in profiles])

@bp.route("/profiles/<int:profile_id>", methods=["GET"])
def get_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    return jsonify({"id": profile.id, "bio": profile.bio, "user_id": profile.user_id})

@bp.route("/profiles/<int:profile_id>", methods=["PUT"])
def update_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    data = request.json
    profile.bio = data.get("bio", profile.bio)
    db.session.commit()
    return jsonify({"id": profile.id, "bio": profile.bio, "user_id": profile.user_id})

@bp.route("/profiles/<int:profile_id>", methods=["DELETE"])
def delete_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    db.session.delete(profile)
    db.session.commit()
    return jsonify({"message": f"Profile {profile_id} deleted"})

# -------------------- AUTHORS --------------------
@bp.route("/authors", methods=["POST"])
def create_author():
    data = request.json
    author = Author(name=data["name"])
    db.session.add(author)
    db.session.commit()
    return jsonify({"id": author.id, "name": author.name})

@bp.route("/authors", methods=["GET"])
def get_authors():
    authors = Author.query.all()
    return jsonify([{"id": a.id, "name": a.name} for a in authors])

@bp.route("/authors/<int:author_id>", methods=["GET"])
def get_author(author_id):
    author = Author.query.get_or_404(author_id)
    return jsonify({"id": author.id, "name": author.name})

@bp.route("/authors/<int:author_id>", methods=["PUT"])
def update_author(author_id):
    author = Author.query.get_or_404(author_id)
    data = request.json
    author.name = data.get("name", author.name)
    db.session.commit()
    return jsonify({"id": author.id, "name": author.name})

@bp.route("/authors/<int:author_id>", methods=["DELETE"])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({"message": f"Author {author_id} deleted"})

# -------------------- BOOKS --------------------
@bp.route("/books", methods=["POST"])
def create_book():
    data = request.json
    book = Book(title=data["title"], author_id=data["author_id"])
    db.session.add(book)
    db.session.commit()
    return jsonify({"id": book.id, "title": book.title})

@bp.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([{"id": b.id, "title": b.title, "author_id": b.author_id} for b in books])

@bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({"id": book.id, "title": book.title, "author_id": book.author_id})

@bp.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.json
    book.title = data.get("title", book.title)
    book.author_id = data.get("author_id", book.author_id)
    db.session.commit()
    return jsonify({"id": book.id, "title": book.title, "author_id": book.author_id})

@bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Book {book_id} deleted"})

# -------------------- STUDENTS --------------------
@bp.route("/students", methods=["POST"])
def create_student():
    data = request.json
    student = Student(name=data["name"])
    db.session.add(student)
    db.session.commit()
    return jsonify({"id": student.id, "name": student.name})

@bp.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([{"id": s.id, "name": s.name} for s in students])

@bp.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify({"id": student.id, "name": student.name})

@bp.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.json
    student.name = data.get("name", student.name)
    db.session.commit()
    return jsonify({"id": student.id, "name": student.name})

@bp.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": f"Student {student_id} deleted"})

# -------------------- COURSES --------------------
@bp.route("/courses", methods=["POST"])
def create_course():
    data = request.json
    course = Course(title=data["title"])
    db.session.add(course)
    db.session.commit()
    return jsonify({"id": course.id, "title": course.title})

@bp.route("/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return jsonify([{"id": c.id, "title": c.title} for c in courses])

@bp.route("/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify({"id": course.id, "title": course.title})

@bp.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.json
    course.title = data.get("title", course.title)
    db.session.commit()
    return jsonify({"id": course.id, "title": course.title})

@bp.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": f"Course {course_id} deleted"})

# -------------------- ENROLL --------------------
@bp.route("/enroll", methods=["POST"])
def enroll_student():
    data = request.json
    student = Student.query.get_or_404(data["student_id"])
    course = Course.query.get_or_404(data["course_id"])
    if course not in student.courses:
        student.courses.append(course)
        db.session.commit()
    return jsonify({"message": f"{student.name} enrolled in {course.title}"})

# -------------------- REGISTRAR BLUEPRINT --------------------
app.register_blueprint(bp)

# -------------------- RUN APP --------------------
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
