import sys
from flask import Flask
from flask.ext import admin, login
from flask.ext.admin import helpers
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface

from pymongo import read_preferences

neobug = Flask(__name__)
neobug.config['UPLOAD_FOLDER'] = 'neobug/static/uploads'

if 'neobug.test.config' in sys.modules:
    neobug.config.from_object(sys.modules['neobug.test.config'])
else:
    neobug.config['MONGODB_SETTINGS'] = {
        'db': 'neobug',
        'read_preference': read_preferences.ReadPreference.PRIMARY
    }
    neobug.config['SECRET_KEY'] = 'KupiKotaZaStoBaksov'

db = MongoEngine(neobug)
neobug.session_interface = MongoEngineSessionInterface(db)
from neobug.models import *
from neobug.admin_views import *
from neobug import views


from blueprints.wiki.views import wiki
from blueprints.projects.views import projects
from blueprints.downloads.views import downloads
from blueprints.downloads.models import Download
neobug.register_blueprint(wiki, url_prefix='/wiki')
neobug.register_blueprint(projects, url_prefix='/projects')
neobug.register_blueprint(downloads, url_prefix='/downloads')


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(neobug)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects.where("this.username=='" + user_id + "'")[0]

init_login()

admin = admin.Admin(neobug, 'neobug', index_view=MyAdminIndexView())
admin.add_view(UserView(User))
admin.add_view(ProjectView(Project))
admin.add_view(IssueView(Issue))
admin.add_view(OverviewView(Overview))
admin.add_view(DownloadView(Download))

if __name__ == "__main__":
    neobug.run()
