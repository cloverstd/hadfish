from werkzeug.contrib.fixers import ProxyFix
from hadfish import app

app.wsgi_app = ProxyFix(app.wsgi_app)
