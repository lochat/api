from flask import Flask
from flask.ext.script import Manager
from lochat.urls import urlpatterns

app = Flask(__name__)
manager = Manager(app)

for urlpattern in urlpatterns:
    rule, view, methods = urlpattern
    app.add_url_rule(rule, view_func=view, methods=methods)

if __name__ == '__main__':
    manager.run()
