from weppy import session, T
from weppy.dal import Field, Model, fieldmethod, modelmethod
from weppy.validators import isntEmpty, isIntInRange


class Campaign(Model):
    tablename = "campaigns"

    fields = [
        Field("owner", "reference auth_user"),
        Field("title", "string"),
        Field("description", "text"),
        Field("start", "datetime"),
        Field("end", "datetime"),
        Field("goal", "integer"),
        Field("closed", "boolean", default=True),
    ]

    visibility = {
        "owner": (False, False),
        "closed": (False, False)
    }
    validators = {
        "title": isntEmpty(),
        "description": isntEmpty(),
        "goal": isIntInRange(1, None)
    }
    labels = {
        "title": T("Title: ")
    }

    @fieldmethod('donations')
    def get_donations(self, row):
        cid = row.campaigns.id
        return self.db(self.db.Donation.campaign == cid).select()

    @fieldmethod('pledged')
    def get_pledge(self, row):
        donations = row.campaigns.donations()
        amount = 0
        for donation in donations:
            amount += donation.amount
        return amount

    @fieldmethod('costs')
    def get_costs(self, row):
        cid = row.campaigns.id
        return self.db(self.db.Cost.campaign == cid).select()

    @fieldmethod('spended')
    def get_spended(self, row):
        costs = row.campaigns.costs()
        amount = 0
        for cost in costs:
            amount += cost.amount
        return amount

    @modelmethod
    def find_owned(db, entity, query=None, owner=None):
        uid = owner or (session.auth.user.id if session.auth else None)
        _query = (entity.owner == uid)
        if query:
            _query = _query & query
        return db(_query).select(orderby=~entity.end)
