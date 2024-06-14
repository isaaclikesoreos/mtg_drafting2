from flask import Blueprint, render_template
from application.models import CardInfo

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    card = CardInfo.query.filter_by(card_name='RAGAVAN, NIMBLE PILFERER').first()
    return render_template('errors/404.html', card=card), 404


@errors.app_errorhandler(403)
def error_403(error):
    card = CardInfo.query.filter_by(card_name='RAGAVAN, NIMBLE PILFERER').first()
    return render_template('errors/403.html', card=card), 403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/404.html'), 500

