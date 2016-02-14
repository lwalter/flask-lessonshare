from lessonshare.core.models import CRUDMixin, BaseRecordMixin
from lessonshare import app, db


class LessonItems(CRUDMixin, BaseRecordMixin, db.Model):

    __tablename__ = 'lesson_items'

    content = db.Column(db.String(500), unique=False)
    lesson_plan = db.Column(db.Integer, db.ForeignKey('lesson_plan.id'), nullable=False)

    def __init__(self, content, lesson_plan):
        super(self.__class__, self).__init__()

        self.content = content
        self.lesson_plan = lesson_plan

    def __repr__(self):
        return '<LessonItem {0}>'.format(self.content)

    @property
    def serialize(self):
        return {
            'content': self.content
        }

    @staticmethod
    def get_serialized_lesson_items(lesson_plan_id, created_by):
        lesson_items = LessonItems.query.filter_by(lesson_plan=lesson_plan_id, created_by=created_by).all()

        return [item.serialize for item in lesson_items]
