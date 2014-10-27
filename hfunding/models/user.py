from weppy import Field
from weppy.dal.models import AuthModel, fieldmethod


class User(AuthModel):
    fields = [
        Field("money", "integer", default=0),
        Field("avatar", "upload", uploadfolder='uploads'),
    ]

    profile_visibility = {
        "avatar": (True, True)
    }

    @fieldmethod('campaigns')
    def get_campaigns(self, row):
        return self.db.Campaign._find_owned(owner=row.auth_user.id)

    @fieldmethod('donations')
    def get_donations(self, row):
        return self.db.Donation._find_owned(owner=row.auth_user.id)

    @fieldmethod('backed_campaigns')
    def get_backed_campaigns(self, row):
        campaigns = self.db(
            self.db.Donation.donator == row.auth_user.id
        ).select(
            self.db.Donation.campaign, groupby=self.db.Donation.campaign
        )
        return len(campaigns)

    @fieldmethod('backed_amount')
    def get_backed_amount(self, row):
        total = self.db.Donation.amount.sum()
        row = self.db(self.db.Donation.donator == row.auth_user.id).select(
            total, groupby=self.db.Donation.donator).first()
        if row:
            return row._extra[total]
        return 0
