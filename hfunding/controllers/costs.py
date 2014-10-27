from weppy import url, redirect
from weppy.tools import requires
from hfunding import app, db, auth, Cost


@app.expose("/costs/<int:campaign>")
def of(campaign):
    costs = db(db.Cost.campaign == campaign).select()
    return dict(costs=costs)


@app.expose("/costs/<int:campaign>/add")
@requires(auth.is_logged_in, url('main.account', 'login'))
def add(campaign):
    def validate(form):
        if form.vars.amount > record.pledged():
            form.errors.amount = ""
    message = None
    record = db.Campaign(id=campaign, owner=auth.user.id)
    if not record:
        message = "Bad campaign id"
    form = Cost.form(onvalidation=validate)
    form.vars.campaign = record.id
    if form.accepted:
        redirect(url('campaigns.detail', record.id))
    return dict(msg=message, form=form)
