from app import create_app, db
from blueprint.home_bp import home_page
from blueprint.record_bp import record_page
from blueprint.setting.category_bp import categrory_page
from blueprint.setting.setting_bp import setting_page
from blueprint.setting.subject_bp import subject_page
from blueprint.sign_bp import sign_page
from blueprint.upload_bp import upload_page

app = create_app()

app.register_blueprint(home_page, url_prefix="/")
app.register_blueprint(upload_page, url_prefix="/upload")
app.register_blueprint(setting_page, url_prefix="/setting")
app.register_blueprint(categrory_page, url_prefix="/setting/category")
app.register_blueprint(subject_page, url_prefix="/setting/subject")
app.register_blueprint(sign_page, url_prefix="/sign")
app.register_blueprint(record_page, url_prefix="/record")

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
