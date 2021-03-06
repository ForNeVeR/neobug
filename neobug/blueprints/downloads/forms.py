from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *

from models import Download

BaseDownloadForm = model_form(Download, exclude=['md5sum', 'sha1sum'])


class DownloadForm(BaseDownloadForm):
    url = FileField('File to upload')
