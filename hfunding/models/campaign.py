from weppy import T, request
from weppy.dal import Field, Model, belongs_to, has_many, fieldmethod


class Campaign(Model):
    belongs_to('user')
    has_many('donations', 'costs')

    title = Field('string', notnull=True)
    description = Field('string', notnull=True)
    start = Field('datetime')
    end = Field('datetime')
    goal = Field('int')
    closed = Field('bool', default=True)

    form_rw = {
        "user": False,
        "closed": False
    }

    validation = {
        "goal": {'gt': 1},
        "start": {'gt': lambda: request.now, 'format': "%d/%m/%Y %H:%M:%S"},
        "end": {'gt': lambda: request.now, 'format': "%d/%m/%Y %H:%M:%S"}
    }

    form_labels = {
        "title": T("Title: ")
    }

    @fieldmethod('pledged')
    def get_pledge(self, row):
        donations = row.campaigns.donations()
        amount = 0
        for donation in donations:
            amount += donation.amount
        return amount

    @fieldmethod('spended')
    def get_spended(self, row):
        costs = row.campaigns.costs()
        amount = 0
        for cost in costs:
            amount += cost.amount
        return amount
