from unarea_core.session.resources import SessionDocument
from unarea_core.session.models import SessionModel
from unarea_core.users.bins import USER_MODEL

SESSION_MODEL = SessionModel(SessionDocument(), USER_MODEL)