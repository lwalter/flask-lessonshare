from flask.ext.restful import Resource, reqparse
from flask_jwt import current_identity, jwt_required
from .models import LessonItems
from lessonshare.lessonplans.models import LessonPlans


class LessonItemsAPI(Resource):
    decorators = [jwt_required()]

    def get(self, id):

        if not id:
            return {'description': 'Invalid parameters.'}, 400

        if not LessonPlans.query.get(id):
            return {'description': 'No lesson plan exists with that id.'}, 400

        return LessonItems.get_serialized_lesson_items(id, current_identity.id), 200

    def post(self, id):

        if not id:
            return {'description': 'Invalid parameters.'}, 400

        reqparser = reqparse.RequestParser()
        reqparser.add_argument('title', type=str, help='No title provided', location='json')
        reqparser.add_argument('content', type=str, help='No content provided', location='json')

        args = reqparser.parse_args()

        # TODO(lnw) refactor common check methods
        lesson_plan = LessonPlans.query.get(id)

        if not lesson_plan:
            return {'description': 'No lesson plan exists with that id.'}, 400

        if lesson_plan.created_by != current_identity.id:
            return {'description': 'You cannot modify that lesson item.'}, 403

        try:
            lesson_item = LessonItems(title=args.get('title'), content=args.get('content'), lesson_plan=id)
            lesson_item.save()
        except Exception, e:
            # TODO(lnw) really need to add a logger...
            return {'description': 'Could not save the lesson item.'}, 500

        return LessonItems.get_serialized_lesson_items(id, current_identity.id), 201

    def delete(self, id):

        if not id:
            return {'description': 'Invalid parameters.'}, 400

        lesson_item = LessonItems.query.get(id)

        if not lesson_item:
            return {'description': 'No lesson item exists.'}, 400

        if lesson_item.created_by != current_identity.id:
            return {'description': 'You cannot modify that lesson item.'}, 403

        try:
            lesson_item.delete()
        except Exception, e:
            return {'description': 'Could not delete the lesson item.'}, 500

        return LessonItems.get_serialized_lesson_items(lesson_item.lesson_plan, current_identity.id), 200