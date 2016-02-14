from flask.ext.restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from .models import LessonPlans


class LessonPlansAPI(Resource):
    decorators = [jwt_required()]

    def get(self):
        return LessonPlans.get_serialized_plans_by_owner(current_identity.id), 200

    def post(self):

        reqparser = reqparse.RequestParser()
        reqparser.add_argument('title', type=str, required=True, help='No title provided', location='json')
        reqparser.add_argument('description', type=str, required=True, help='No description provided', location='json')

        args = reqparser.parse_args()

        new_lesson_plan = LessonPlans(title=args.get('title'),
                                      description=args.get('description'))

        try:
            new_lesson_plan.save()
        except Exception, e:
            return {'description': 'Server encountered an error.'}, 500

        return LessonPlans.get_serialized_plans_by_owner(current_identity.id), 201

    def delete(self, id):

        if not id:
            return {'description': 'No id provided.'}, 400

        lesson_plan = LessonPlans.query.filter_by(created_by=current_identity.id, id=id).first()

        if not lesson_plan:
            return {'description': 'You are not the owner of this lesson plan.'}, 403

        try:
            lesson_plan.delete()
        except Exception, e:
            return {'description': 'Server encountered an error.'}, 500

        return LessonPlans.get_serialized_plans_by_owner(current_identity.id), 200

    def put(self, id):

        if not id:
            return {'description': 'No id provided.'}, 400

        reqparser = reqparse.RequestParser()
        reqparser.add_argument('title', type=str, help='No title provided', location='json')
        reqparser.add_argument('description', type=str, help='No description provided', location='json')

        args = reqparser.parse_args()

        lesson_plan = LessonPlans.query.filter_by(created_by=current_identity.id, id=id).first()

        if not lesson_plan:
            return {'description': 'You are not the owner of this lesson plan.'}, 403

        try:
            title = args.get('title', None)
            description = args.get('description', None)

            lesson_plan.title = lesson_plan.title if title is None else title
            lesson_plan.description = lesson_plan.description if description is None else description

            lesson_plan.save()
        except Exception, e:
            return {'description': 'Server encountered an error.'}, 500

        return lesson_plan.serialize, 200
