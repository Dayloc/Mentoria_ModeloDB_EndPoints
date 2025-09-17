from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Table

db = SQLAlchemy()



# ------------------ RELACIÓN 1:1 ------------------
class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False)


class Profile(db.Model):
    __tablename__ = 'profiles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bio: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship("User", back_populates="profile")


# ------------------ RELACIÓN 1:N ------------------
class Author(db.Model):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Book(db.Model):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))

    author: Mapped[Author] = relationship("Author", back_populates="books")


# ------------------ RELACIÓN N:N ------------------

# Tabla de relación para N:N
student_course = Table(
    'student_course',
    db.metadata,
    db.Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True)
)
class Student(db.Model):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    courses: Mapped[list["Course"]] = relationship(
        "Course",
        secondary=student_course,
        back_populates="students"
    )


class Course(db.Model):
    __tablename__ = 'courses'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    students: Mapped[list[Student]] = relationship(
        "Student",
        secondary=student_course,
        back_populates="courses"
    )
