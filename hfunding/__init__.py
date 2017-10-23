from weppy import App
from weppy.orm import Database
from weppy.tools import Auth
from weppy.sessions import SessionManager

## init our app
app = App(__name__)
app.config.static_version = '0.1.0'
app.config.static_version_urls = True
app.config.url_default_namespace = "main"
app.config.auth.hmac_key = "99b2fdd8-3622-4237-9f1b-9ce4445045d9"
app.config.auth.registration_verification = False
app.config.auth.single_template = True

## language settings
app.languages = ['en', 'it']
app.language_default = 'en'
app.language_force_on_url = True
app.language_write = True

## init database and auth
from models.user import User
from models.campaign import Campaign
from models.donation import Donation
from models.cost import Cost
## init auth before passing db models due to dependencies
## on auth tables in the other models
db = Database(app, auto_migrate=True)
auth = Auth(app, db, user_model=User)
# auth.settings.update(download_url='/download')
db.define_models(Campaign, Donation, Cost)

## adding sessions and authorization handlers
app.pipeline = [
    SessionManager.cookies('verySecretKey'),
    db.pipe,
    auth.pipe
]

## add esxtensions
from weppy_haml import Haml
from weppy_assets import Assets
from weppy_bs3 import BS3
app.config.Haml.set_as_default = True
# app.config.Haml.auto_reload = True
app.use_extension(Haml)
app.config.Assets.out_folder = 'gen'
app.use_extension(Assets)
app.use_extension(BS3)

## exposing functions from controllers
auth_routes = auth.module(__name__, url_prefix='account')

from controllers import main, campaigns, donations, costs


## assets
js_libs = app.ext.Assets.js(
    ['js/masonry.min.js'],
    output='libs.js')
css = app.ext.Assets.css(
    ['css/bootstrap-theme.min.css',
     'css/app.css'],
    output='common.css')
app.ext.Assets.register('js_libs', js_libs)
app.ext.Assets.register('css_all', css)


## commands
@app.cli.command('cron')
def runcron():
    from datetime import datetime
    import time
    while True:
        db._adapter.reconnect()
        db(
            (db.Campaign.start <= datetime.now()) &
            (db.Campaign.end > datetime.now()) &
            (db.Campaign.closed == True)
        ).update(closed=False)
        db.commit()
        db(
            (db.Campaign.end <= datetime.now()) &
            (db.Campaign.closed == False)
        ).update(closed=True)
        db.commit()
        print "sleeping.."
        time.sleep(60)
