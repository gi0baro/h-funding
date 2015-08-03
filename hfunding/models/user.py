from weppy.dal import Field, has_many, fieldmethod
from weppy.tools.auth.models import AuthUser


class User(AuthUser):
    has_many('campaigns', 'donations')

    money = Field('int', default=0)
    avatar = Field('upload', uploadfolder='uploads')

    form_profile_rw = {
        "avatar": True
    }

    @fieldmethod('backed_campaigns')
    def get_backed_campaigns(self, row):
        campaigns = self.db(
            self.db.Donation.user == row.users.id
        ).select(
            self.db.Donation.campaign, groupby=self.db.Donation.campaign
        )
        return len(campaigns)

    @fieldmethod('backed_amount')
    def get_backed_amount(self, row):
        total = self.db.Donation.amount.sum()
        row = self.db(self.db.Donation.user == row.users.id).select(
            total, groupby=self.db.Donation.user).first()
        if row:
            return row._extra[total]
        return 0
