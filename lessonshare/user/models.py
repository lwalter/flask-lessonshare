from lessonshare import db, bcrypt
from lessonshare.core.models import CreatedAtMixin, IdMixin, CRUDMixin


class Users(CRUDMixin, IdMixin, CreatedAtMixin, db.Model):

    __tablename__ = 'users'

    email = db.Column(db.String(200), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    lesson_plans = db.relationship('LessonPlans', backref=db.backref('users'), lazy='dynamic')

    def __init__(self, email, password, first_name, last_name):
        super(self.__class__, self).__init__()

        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User {0}>'.format(self.email)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
