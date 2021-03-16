from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/barsuxDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '101111010101010100100101000100000001011011100101001010101001000011111'
db = SQLAlchemy(app)


from ALCU import models, routes
db.create_all()





