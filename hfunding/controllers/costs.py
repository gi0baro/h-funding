from weppy import url, redirect
from weppy.tools import requires
from hfunding import app, auth, Cost, Campaign


@app.route("/costs/<int:campaign>")
def of(campaign):
    costs = Cost.where(lambda c: c.campaign == campaign).select()
    return dict(costs=costs)


@app.route("/costs/<int:campaign>/add")
@requires(auth.is_logged_in, url('main.account', 'login'))
def add(campaign):
    def validate(form):
        if form.params.amount > record.pledged():
            form.errors.amount = ""
    message = None
    record = Campaign.get(id=campaign, user=auth.user.id)
    if not record:
        message = "Bad campaign id"
    form = Cost.form(onvalidation=validate)
    form.params.campaign = record.id
    if form.accepted:
        redirect(url('campaigns.detail', record.id))
    return dict(msg=message, form=form)
