from lessonshare import db
from lessonshare.core.models import BaseRecordMixin, CRUDMixin


class LessonPlans(CRUDMixin, BaseRecordMixin, db.Model):

    __tablename__ = 'lesson_plan'

    title = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    likes = db.Column(db.Integer)

    lesson_items = db.relationship('LessonItems', backref=db.backref('lesson_items'), cascade='all, delete-orphan',
                                   lazy='dynamic')

    def __init__(self, title, description):
        super(self.__class__, self).__init__()

        self.likes = 0
        self.title = title
        self.description = description

    def __repr__(self):
        return '<LessonPlan {0}>'.format(self.title)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'likes': self.likes,
            'created_at': self.created_at.isoformat(),
            'created_by': self.created_by
        }

    @staticmethod
    def get_serialized_plans_by_owner(owner_id):
        user_lesson_plans = LessonPlans.query.filter_by(created_by=owner_id).order_by(LessonPlans.created_at.desc())
        return [plan.serialize for plan in user_lesson_plans]
