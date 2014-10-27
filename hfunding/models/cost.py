from weppy.dal.models import Model, modelmethod
from weppy import Field, session, request
from weppy.validators import IS_NOT_EMPTY, IS_INT_IN_RANGE


class Cost(Model):
    tablename = "costs"

    fields = [
        Field("campaign", "reference campaigns"),
        Field("name", "string"),
        Field("date", "datetime", default=lambda: request.now),
        Field("amount", "integer")
    ]

    visibility = {
        "campaign": (False, False),
        "date": (False, True)
    }
    validators = {
        "name": IS_NOT_EMPTY(),
        "amount": IS_INT_IN_RANGE(1, None)
    }

    @modelmethod
    def find_owned(db, entity, query=None, owner=None):
        uid = owner or (session.auth.user.id if session.auth else None)
        _query = (entity.donator == uid)
        if query:
            _query = _query & query
        return db(_query).select()
