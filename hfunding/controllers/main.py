from weppy import Form, Field, response, url, abort, redirect
from weppy.helpers import stream_dbfile
from weppy.tools import requires
from .. import app, db, auth, User, Campaign, Donation


@app.on_error(404)
def error_404():
    return app.render_template('404.haml')


@app.route("/")
def welcome():
    response.meta.title = "HFunding"
    return dict()


@app.route("/users", template='users.haml')
def users():
    response.meta.title = "HFunding | Bakers"
    return dict(users=User.all().select())


@app.route("/user/<str:userid>")
def profile(userid):
    user = User.get(userid)
    if not user:
        abort(404)
    response.meta.title = "HFunding | " + user.first_name + " " + \
        user.last_name + " profile"
    return dict(user=user)


@app.route()
@requires(auth.is_logged, url('auth.login'))
def charge():
    response.meta.title = "HFunding | Charge account"
    form = Form(amount=Field.int())
    if form.accepted:
        auth.user.update_record(
            money=auth.user.money + int(form.params.amount))
        redirect(url('main.profile', auth.user.id))
    return dict(form=form)


@app.route()
def stats():
    response.meta.title = "HFunding | Stats"
    money_total = Donation.amount.sum()
    campaigns = db(Donation.campaign == Campaign.id).select(
        Campaign.id, Campaign.title, Campaign.goal, money_total,
        groupby=Campaign.id, orderby=money_total
    )
    ## total pledged and campaigns reached 100%
    total_pledged = 0
    success_campaigns = 0
    for row in campaigns:
        total_pledged += row[money_total]
        if row.campaigns.goal <= row[money_total]:
            success_campaigns += 1
    if success_campaigns:
        success_campaigns = float(success_campaigns) / len(campaigns) * 100
    ## most succesful campaigns
    top_campaigns = campaigns[:10]
    return dict(total=total_pledged, success=int(round(success_campaigns)),
                top=top_campaigns, mt=money_total)


@app.route("/download/<str:filename>")
def download(filename):
    stream_dbfile(db, filename)
