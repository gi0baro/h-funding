from weppy import now
from weppy.orm import Field, Model, belongs_to


class Donation(Model):
    belongs_to('user', 'campaign')

    date = Field.datetime(default=now)
    amount = Field.int()

    fields_rw = {
        "user": False,
        "campaign": False,
        "date": False
    }

    validation = {
        'amount': {'gt': 1}
    }
