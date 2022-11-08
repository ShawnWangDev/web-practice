from flask import Blueprint, render_template
from flask_login import login_required

setting_page = Blueprint('setting_page', __name__,
                        template_folder='templates')


@setting_page.route('/')
@login_required
def setting_index():
    return render_template('setting/index.html', title="setting")
