from weppy import url, redirect
from weppy.tools import requires
from hfunding import app, db, auth, Donation


@app.expose('/donations/<int:campaign>')
def of(campaign):
    pass


@app.expose('/donations/mine')
@requires(auth.is_logged_in, url('main.account', 'login'))
def owned():
    donations = Donation.find_owned()
    return dict(donations=donations)


@app.expose('/donate/<int:campaign>', template="donate.html")
@requires(auth.is_logged_in, url('main.account', 'login'))
def add(campaign):
    message = None
    record = db.Campaign(id=campaign)
    if not record:
        message = "Bad campaign id"
    form = Donation.form()
    form.vars.donator = auth.user.id
    form.vars.campaign = record.id
    if form.accepted:
        redirect(url('campaigns.detail', record.id))
    return dict(msg=message, form=form, campaign=record)
