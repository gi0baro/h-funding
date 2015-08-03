from weppy import request
from weppy.dal import Field, Model, belongs_to


class Donation(Model):
    belongs_to('user', 'campaign')

    date = Field('datetime', default=lambda: request.now)
    amount = Field('integer')

    form_rw = {
        "user": False,
        "campaign": False,
        "date": False
    }

    validation = {
        'amount': {'gt': 1}
    }
