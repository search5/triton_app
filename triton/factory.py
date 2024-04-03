from flask import Flask
from flask_login import AnonymousUserMixin
import yaml


def create_app(config_filename):
    from triton.models import db, Member
    from triton.routes import board_app
    from flask_login import LoginManager

    app = Flask(__name__)
    app.config.from_file(config_filename, load=yaml.safe_load)

    db.init_app(app)
    login_manager = LoginManager(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.execute(db.select(Member).where(Member.id == user_id)).scalar_one()

    app.register_blueprint(board_app, url_prefix="/board")

    return app
