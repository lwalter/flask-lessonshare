# Import extensions
import os
from flask.ext.assets import Environment, Bundle
from flask.ext.bcrypt import Bcrypt
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from config import Config

# Import Flask
from flask import Flask

app = Flask('lessonshare')
app.config.from_object(os.environ['APP_SETTINGS'])
api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
assets = Environment(app)

js = Bundle('js/lessonShareApp.js',
            Config.CONTROLLERS_PATH.format('createPlanController.js'), Config.CONTROLLERS_PATH.format('lessonPlanController.js'),
            Config.CONTROLLERS_PATH.format('navbarController.js'), Config.CONTROLLERS_PATH.format('toastController.js'),
            Config.CONTROLLERS_PATH.format('userAuthenticationController.js'), Config.SERVICES_PATH.format('lessonPlanService.js'),
            Config.SERVICES_PATH.format('toastService.js'), Config.SERVICES_PATH.format('userAuthenticationService.js'),
            filters='jsmin', output='jsBundle.js')

css = Bundle(Config.CSS_PATH.format('index.css'), Config.CSS_PATH.format('lesson-plan.css'), Config.CSS_PATH.format('toast.css'),
             Config.CSS_PATH.format('user-auth.css'), filters='cssmin', output='cssBundle.css')

js_libs = Bundle(Config.JS_LIB_PATH.format('angular/angular.js'), Config.JS_LIB_PATH.format('angular-animate/angular-animate.js'),
                 Config.JS_LIB_PATH.format('angular-aria/angular-aria.js'), Config.JS_LIB_PATH.format('angular-material/angular-material.js'),
                 Config.JS_LIB_PATH.format('angular-route/angular-route.js'), Config.JS_LIB_PATH.format('angular-messages/angular-messages.js'),
                 Config.JS_LIB_PATH.format('ngstorage/ngStorage.js'), filters='jsmin', output='jsLibsBundle.js')

css_libs = Bundle(Config.CSS_LIB_PATH.format('angular-material.css'), Config.CSS_LIB_PATH.format('angular-material.layouts.css'),
                  filters='cssmin', output='cssLibs.css')

assets.register('js_angular', js)
assets.register('custom_css', css)
assets.register('js_libs', js_libs)
assets.register('css_libs', css_libs)


# Import blueprints and api resources
from lessonshare.home.views import home
from lessonshare.user.api import UserApi, user_auth, authenticate, identity, payload_handler
from lessonshare.lessonplans.api import LessonPlansAPI
from lessonshare.lessonitems.api import LessonItemsAPI


jwt = JWT(app, authenticate, identity)
jwt.jwt_payload_handler(payload_handler)


app.register_blueprint(home)
app.register_blueprint(user_auth)

api.add_resource(UserApi, '/api/user', endpoint='user')
api.add_resource(LessonPlansAPI, '/api/lessonplans', '/api/lessonplans/<int:id>', endpoint='lessonplans')
api.add_resource(LessonItemsAPI, '/api/lessonitems/<int:id>', endpoint='lessonitems')
