from weppy import response, url, stream_file
from weppy.tools import requires
from hfunding import app, db, auth, Campaign, Donation


@app.on_error(404)
def error_404():
    return app.render_template('404.haml')


@app.expose("/")
def welcome():
    response.meta.title = "HFunding"
    return dict()


@app.expose("/account(/<str:f>)?(/<str:k>)?")
def account(f, k):
    response.meta.title = "HFunding | Account"
    form = auth(f, k)
    return dict(req=f, form=form)


@app.expose("/users", template='users.haml')
def users():
    response.meta.title = "HFunding | Bakers"
    users = db(db.User.id > 0).select()
    return dict(users=users)


@app.expose("/user/<str:userid>")
def profile(userid):
    user = db.User(id=userid)
    campaigns = Campaign.find_owned(owner=user.id)
    donations = Donation.find_owned(owner=user.id)
    response.meta.title = "HFunding | " + user.first_name + " " + \
        user.last_name + " profile"
    return dict(user=user, campaigns=campaigns, donations=donations)


@app.expose()
@requires(auth.is_logged_in, url('main.account', 'login'))
def charge():
    from weppy import Form, Field, redirect
    response.meta.title = "HFunding | Charge account"
    form = Form(
        Field("amount", "integer")
    )
    if form.accepted:
        db.User(id=auth.user.id).update_record(
            money=auth.user.money+int(form.vars.amount))
        auth.user.update(money=auth.user.money+int(form.vars.amount))
        redirect(url('main.profile', auth.user.id))
    return dict(form=form)


@app.expose()
def stats():
    response.meta.title = "HFunding | Stats"
    money_total = db.Donation.amount.sum()
    campaigns = db(db.Donation.campaign == db.Campaign.id).select(
        db.Campaign.id, db.Campaign.title, db.Campaign.goal,
        money_total, groupby=db.Campaign.id, orderby=money_total
    )
    ## total pledged and campaigns reached 100%
    total_pledged = 0
    success_campaigns = 0
    for row in campaigns:
        total_pledged += row._extra[money_total]
        if row.campaigns.goal <= row._extra[money_total]:
            success_campaigns += 1
    if success_campaigns:
        success_campaigns = float(success_campaigns)/len(campaigns)*100
    ## most succesful campaigns
    top_campaigns = campaigns[:10]
    return dict(total=total_pledged, success=int(round(success_campaigns)),
                top=top_campaigns, mt=money_total)


@app.expose("/download/<str:filename>")
def download(filename):
    stream_file(db, filename)
