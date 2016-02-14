from flask.ext.restful import Resource, reqparse
from flask_jwt import current_identity, jwt_required
from .models import LessonItems
from lessonshare.lessonplans.models import LessonPlans


class LessonItemsAPI(Resource):
    decorators = [jwt_required()]

    def get(self, lesson_plan_id):
        if not lesson_plan_id:
            return {'description': 'Invalid parameters.'}, 401

        if not LessonPlans.query.get(lesson_plan_id):
            return {'description': 'No lesson plan exists with that id.'}, 400

        return LessonItems.get_serialized_lesson_items(lesson_plan_id, current_identity.id), 200

    def post(self, lesson_plan_id):
        if not lesson_plan_id:
            return {'description': 'Invalid parameters.'}, 401

        reqparser = reqparse.RequestParser()
        reqparser.add_argument('content', type=str, help='No content provided', location='json')

        args = reqparser.parse_args()

        # TODO(lnw) refactor common check methods
        if not LessonPlans.query.get(lesson_plan_id):
            return {'description': 'No lesson plan exists with that id.'}, 400

        try:
            lesson_item = LessonItems(content=args.get('content'), lesson_plan=lesson_plan_id)
            lesson_item.save()
        except Exception, e:
            # TODO(lnw) really need to add a logger...
            return {'description': 'Could not save the lesson item.'}

        return LessonItems.get_serialized_lesson_items(lesson_plan_id, current_identity.id), 201
