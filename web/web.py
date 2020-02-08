from flask import Flask
from users_controller import usersBlueprint

app = Flask(__name__)
app.register_blueprint(usersBlueprint)


app.run(use_reloader=True, debug=True)