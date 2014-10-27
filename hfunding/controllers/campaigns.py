from weppy import AppModule, request, url, redirect, asis
from weppy.tools import requires
from hfunding import app, db, auth, Campaign, Cost

campaigns = AppModule(app, 'campaigns', __name__, url_prefix='campaigns',
                      template_folder='campaigns')


@campaigns.expose('/', template="discover.html")
def discover():
    campaigns = db(
        (db.Campaign.start <= request.now) & (db.Campaign.closed == False)
    ).select(
        orderby=~db.Campaign.start,
        limitby=(0, 20)
    )
    return dict(campaigns=campaigns, showing='discover')


@campaigns.expose(template="discover.html")
def all():
    campaigns = db(db.Campaign.start <= request.now).select(
        orderby=~db.Campaign.start,
        limitby=(0, 20)
    )
    return dict(campaigns=campaigns, showing='all')


@campaigns.expose('/mine', template="mine.html")
@requires(auth.is_logged_in, url('main.account', 'login'))
def owned():
    campaigns = Campaign.find_owned()
    return locals()


@campaigns.expose(template='manage.html')
@requires(auth.is_logged_in, url('main.account', 'login'))
def new():
    form = Campaign.form()
    form.input_vars.owner = auth.user.id
    if form.accepted:
        redirect(url('main.profile', auth.user.id))
    return locals()


@campaigns.expose('/edit/<int:cid>', template='manage.html')
@requires(auth.is_logged_in, url('main.account', 'login'))
def edit(cid):
    #form = db.Campaign._form()
    #return locals()
    return dict()


@campaigns.expose('/destroy/<int:cid>')
@requires(auth.is_logged_in, url('main.account', 'login'))
def destroy(cid):
    #form = db.Campaign._form()
    #return locals()
    return dict()


@campaigns.expose('/<int:cid>')
def detail(cid):
    def validate_cost(form):
        if form.vars.amount > (campaign.pledged()-campaign.spended()):
            form.errors.amount = \
                "The amount inserted is bigger than the amount pledged."

    campaign = db.Campaign(id=cid)
    cost_form = Cost.form(onvalidation=validate_cost)
    cost_form.vars.campaign = campaign.id
    #if cost_form.process(keepvalues=True).accepted:
    if cost_form.accepted:
        redirect(url('campaigns.detail', cid))
    return dict(campaign=campaign, cost_form=cost_form, graph=graph_data)


def graph_data(campaign):
    donations = db(db.Donation.campaign == campaign.id).select(
        orderby=db.Donation.date)
    costs = db(db.Cost.campaign == campaign.id).select(orderby=db.Cost.date)
    inf = []
    for row in donations:
        inf.append(("don", row))
    for row in costs:
        inf.append(("cos", row))
    inf.sort(key=lambda d: d[1].date)
    countD = 0
    countC = 0
    data = []
    for t, row in inf:
        if t == "don":
            countD += row.amount
            data.append([str(row.date), int(countD),
                         row.donator.first_name, int(countC), ""])
        else:
            countC += row.amount
            data.append([str(row.date), int(countD), "",
                         int(countC), row.name])
    data.append(["", data[-1][1], "", data[-1][3], ""])
    return asis(str(data))
