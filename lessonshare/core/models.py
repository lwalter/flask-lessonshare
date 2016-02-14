from datetime import datetime
from lessonshare import db
from flask_jwt import current_identity
from sqlalchemy.ext.declarative import declared_attr


class CreatedByMixin(object):

    @declared_attr
    def created_by(self):
        return db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self):
        self.created_by = current_identity.id

    def __repr__(self):
        return '<CreatedByMixin {0}>'.format(self.created_by)


class CreatedAtMixin(object):

    @declared_attr
    def created_at(self):
        return db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<CreatedAtMixin {0}>'.format(self.created_at)


class IdMixin(object):

    @declared_attr
    def id(self):
        return db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)

    def __repr__(self):
        return '<IdMixin {0}>'.format(self.id)


class BaseRecordMixin(IdMixin, CreatedAtMixin, CreatedByMixin):

    def __init__(self):
        CreatedAtMixin.__init__(self)
        CreatedByMixin.__init__(self)

    def __repr__(self):
        return '<BaseRecordMixin {0}>'.format(self.id)


class CRUDMixin(object):

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
