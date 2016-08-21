from weppy.dal import Field, has_many, rowmethod
from weppy.tools.auth.models import AuthUser


class User(AuthUser):
    has_many('campaigns', 'donations')

    money = Field('int', default=0)
    avatar = Field('upload', uploadfolder='uploads')

    form_profile_rw = {
        "avatar": True
    }

    @rowmethod('backed_campaigns')
    def get_backed_campaigns(self, row):
        count = self.db.Donation.campaign.count()
        return (
            row.donations(
                count, groupby=self.db.Donation.campaign).first() or {}
        ).get(count) or 0

    @rowmethod('backed_amount')
    def get_backed_amount(self, row):
        total = self.db.Donation.amount.sum()
        return (
            self.db(self.db.Donation.user == row.id).select(
                total, groupby=self.db.Donation.user).first() or {}
        ).get(total) or 0
