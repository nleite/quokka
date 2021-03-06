# coding: utf-8
from flask.ext.mail import Mail
from flask.ext.cache import Cache
from flask.ext.security import Security, MongoEngineUserDatastore

from dealer.contrib.flask import Dealer
from quokka.core.db import db
from quokka.core.admin import configure_admin
from quokka.modules.accounts.models import Role, User

from . import (generic, babel, blueprints, error_handlers, context_processors,
               template_filters, before_request, views, themes, fixtures)


def configure_extensions(app, admin):
    babel.configure(app)
    generic.configure(app)
    Cache(app)
    Mail(app)
    Dealer(app)
    error_handlers.configure(app)
    db.init_app(app)
    fixtures.configure(app)
    themes.configure(app, db)  # Themes should be configured after db

    context_processors.configure(app)
    template_filters.configure(app)

    user_datastore = MongoEngineUserDatastore(db, User, Role)
    Security(app, user_datastore)

    blueprints.load_from_packages(app)
    blueprints.load_from_folder(app)

    configure_admin(app, admin)

    if app.config.get('DEBUG_TOOLBAR_ENABLED'):
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            DebugToolbarExtension(app)
        except:
            pass

    before_request.configure(app)
    views.configure(app)

    return app
