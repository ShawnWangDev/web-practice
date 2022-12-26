from flask import Blueprint, render_template

from blueprint.sign_bp import SigninForm
from flask_login import current_user
import service.setting.subject_serv as subject_serv

home_page = Blueprint('home_page', __name__,
                    template_folder='templates')


@home_page.route('/')
def index():
    form = SigninForm()
    subject_info_list = None
    if current_user.get_id():
        subject_info_list = subject_serv.all_info_get_by_user_id(
            current_user.id)
    return render_template('index.html', title='home', form=form, subject_info=subject_info_list)
