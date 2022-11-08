from datetime import datetime
from os import makedirs
from pathlib import Path
from uuid import uuid1

from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

import service.upload_file_serv as upload_file_serv
from app import myconfig
from models.upload_file import UploadFile

upload_page = Blueprint('upload_page', __name__,
                        template_folder='templates/upload')


class AttachmentForm(FlaskForm):
    attachment = FileField('Your attachment', validators=[
                        FileRequired(), FileAllowed(['jpg', 'png', 'webp', 'mp4', 'm4v'], "media file only")])


UPLOAD_ROOT_DIR = myconfig['UPLOAD_ROOT_DIR']


@upload_page.route('/', methods=('GET', 'POST'))
def index():
    form = AttachmentForm()
    if form.validate_on_submit():
        uploaded_file = upload_file_to_disk(form.attachment.data)
        if not uploaded_file==None:
            upload_file_serv.add(uploaded_file)
        return redirect(url_for('upload_page.index'))
    return render_template('upload/index.html', title="upload", form=form)


def upload_file_to_disk(f: FileStorage) -> UploadFile:
    year_month_dir = datetime.now().strftime(r'%Y-%m')
    upload_dir = Path(UPLOAD_ROOT_DIR).joinpath(year_month_dir)
    if not upload_dir.exists():
        makedirs(upload_dir)
    datetime_now = datetime.now().strftime(r'%Y%m%d_%H%M%S')
    f.filename = f'{datetime_now}_{uuid1()}{Path(f.filename).suffix}'
    secured_filename = secure_filename(f.filename)
    f.save(upload_dir.joinpath(secured_filename))
    return UploadFile(year_month_dir, secured_filename)
