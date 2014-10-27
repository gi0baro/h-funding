from weppy.dal.models import Model, modelmethod
from weppy import Field, session, request
from weppy.validators import IS_INT_IN_RANGE


class Donation(Model):
    tablename = "donations"

    fields = [
        Field("donator", "reference auth_user"),
        Field("campaign", "reference campaigns"),
        Field("date", "datetime", default=lambda: request.now),
        Field("amount", "integer")
    ]

    visibility = {
        "donator": (False, False),
        "campaign": (False, False),
        "date": (False, False)
    }
    validators = {
        "amount": IS_INT_IN_RANGE(1, None)
    }

    @modelmethod
    def find_owned(db, entity, query=None, owner=None):
        uid = owner or (session.auth.user.id if session.auth else None)
        _query = (entity.donator == uid)
        if query:
            _query = _query & query
        return db(_query).select()
