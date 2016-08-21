from weppy import url, redirect
from weppy.tools import requires
from hfunding import app, auth, Campaign, Donation


@app.route('/donations/<int:campaign>')
def of(campaign):
    pass


@app.route('/donations/mine')
@requires(auth.is_logged_in, url('main.account', 'login'))
def owned():
    donations = auth.user.donations()
    return dict(donations=donations)


@app.route('/donate/<int:campaign>', template="donate.html")
@requires(auth.is_logged_in, url('main.account', 'login'))
def add(campaign):
    def set_form(form):
        form.params.user = auth.user.id
        form.params.campaign = record.id

    message = None
    record = Campaign.get(campaign)
    if not record:
        message = "Bad campaign id"
    form = Donation.form(onvalidation=set_form)
    if form.accepted:
        redirect(url('campaigns.detail', record.id))
    return dict(msg=message, form=form, campaign=record)
