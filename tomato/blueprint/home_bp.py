from flask import Blueprint, render_template

from blueprint.sign_bp import SigninForm

home_page = Blueprint('home_page', __name__,
                    template_folder='templates')


@home_page.route('/')
def index():
    form = SigninForm()
    return render_template('index.html', title='home', form=form)
