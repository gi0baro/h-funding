from weppy import request
from weppy.dal import Field, Model, belongs_to


class Cost(Model):
    belongs_to('campaign')

    name = Field(notnull=True)
    date = Field('datetime', default=lambda: request.now)
    amount = Field('integer')

    form_rw = {
        "campaign": False,
        "date": False
    }

    validation = {
        'amount': {'gt': 1}
    }
