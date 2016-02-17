from lessonshare.core.models import CRUDMixin, BaseRecordMixin
from lessonshare import db


class LessonItems(CRUDMixin, BaseRecordMixin, db.Model):

    __tablename__ = 'lesson_items'

    title = db.Column(db.String(256), unique=False, nullable=False)
    content = db.Column(db.String(500), unique=False)
    lesson_plan = db.Column(db.Integer, db.ForeignKey('lesson_plan.id'), nullable=False)

    def __init__(self, title, content, lesson_plan):
        super(self.__class__, self).__init__()

        self.title = title
        self.content = content
        self.lesson_plan = lesson_plan

    def __repr__(self):
        return '<LessonItem {0}>'.format(self.title)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }

    @staticmethod
    def get_serialized_lesson_items(lesson_plan_id, created_by):
        lesson_items = LessonItems.query.filter_by(lesson_plan=lesson_plan_id, created_by=created_by).all()

        return [item.serialize for item in lesson_items]
