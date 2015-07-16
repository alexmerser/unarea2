from flask import Blueprint
from unarea_accounts.service import USER_ACCOUNT_API

ACCOUNTS = Blueprint('accounts', __name__, url_prefix='/api/v1/accounts')

USER_ACCOUNT_API.init_app(ACCOUNTS)