from weppy import AppModule, request, url, redirect, asis
from weppy.tools import requires
from hfunding import app, auth, Campaign, Cost, Donation

campaigns = AppModule(
    app, 'campaigns', __name__, url_prefix='campaigns',
    template_folder='campaigns')


@campaigns.route('/')
def discover():
    campaigns = Campaign.where(
        lambda c: (c.start <= request.now) & (c.closed == False)
    ).select(orderby=~Campaign.start, paginate=(1, 20))
    return dict(campaigns=campaigns, showing='discover')


@campaigns.route(template="discover.haml")
def all():
    campaigns = Campaign.where(lambda c: c.start <= request.now).select(
        orderby=~Campaign.start, paginate=(1, 20)
    )
    return dict(campaigns=campaigns, showing='all')


@campaigns.route('/mine', template="mine.haml")
@requires(auth.is_logged_in, url('main.account', 'login'))
def owned():
    campaigns = auth.user.campaigns()
    return locals()


@campaigns.route(template='manage.haml')
@requires(auth.is_logged_in, url('main.account', 'login'))
def new():
    def set_owner(form):
        form.params.user = auth.user.id

    form = Campaign.form(onvalidation=set_owner)
    if form.accepted:
        redirect(url('main.profile', auth.user.id))
    return locals()


@campaigns.route('/edit/<int:cid>', template='manage.haml')
@requires(auth.is_logged_in, url('main.account', 'login'))
def edit(cid):
    #form = db.Campaign._form()
    #return locals()
    return dict()


@campaigns.route('/destroy/<int:cid>')
@requires(auth.is_logged_in, url('main.account', 'login'))
def destroy(cid):
    #form = db.Campaign._form()
    #return locals()
    return dict()


@campaigns.route('/<int:cid>')
def detail(cid):
    def validate_cost(form):
        form.params.campaign = campaign.id
        if form.params.amount > (campaign.pledged() - campaign.spended()):
            form.errors.amount = \
                "The amount inserted is bigger than the amount pledged."

    campaign = Campaign.get(cid)
    cost_form = Cost.form(onvalidation=validate_cost)
    if cost_form.accepted:
        redirect(url('campaigns.detail', cid))
    return dict(campaign=campaign, cost_form=cost_form, graph=graph_data)


def graph_data(campaign):
    donations = Donation.where(lambda d: d.campaign == campaign.id).select(
        orderby=Donation.date, including='user')
    costs = Cost.where(lambda c: c.campaign == campaign.id).select(
        orderby=Cost.date)
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
                         row.user.first_name, int(countC), ""])
        else:
            countC += row.amount
            data.append([str(row.date), int(countD), "",
                         int(countC), row.name])
    data.append(["", data[-1][1], "", data[-1][3], ""])
    return asis(str(data))
