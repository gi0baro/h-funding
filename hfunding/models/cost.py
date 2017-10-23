from weppy import now
from weppy.orm import Field, Model, belongs_to


class Cost(Model):
    belongs_to('campaign')

    name = Field(notnull=True)
    date = Field.datetime(default=now)
    amount = Field.int()

    fields_rw = {
        "campaign": False,
        "date": False
    }

    validation = {
        'amount': {'gt': 1}
    }
