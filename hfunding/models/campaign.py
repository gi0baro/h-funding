from weppy import T, request
from weppy.dal import Field, Model, belongs_to, has_many, rowmethod


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

    @rowmethod('pledged')
    def get_pledge(self, row):
        summed = self.db.Donation.amount.sum()
        return row.donations(summed).first()[summed] or 0

    @rowmethod('spended')
    def get_spended(self, row):
        summed = self.db.Cost.amount.sum()
        return row.costs(summed).first()[summed] or 0
