# going to do the baseline stuff from the news app tutorial with flask so i at least have something to start out with.

from flask import Flask, render_template
from peewee import *
app = Flask(__name__)

db = SqliteDatabase('solid_waste.db')
db.connect()

class Violation(Model):
    site_no = CharField()
    site_name = CharField()
    street_address = CharField()
    city_state_zip = CharField()
    county = CharField()
    media = CharField()
    violation_date = DateField()
    status = CharField()
    resolved_date = DateField()
    uuid = CharField(primary_key=True, unique=True)

    class Meta:
        table_name = "violations"
        database = db

@app.route("/")
def index():
    template = 'index.html'
    return render_template(template)

@app.route("/violation/<int:uuid>")
def detail(uuid):
    template = 'detail.html'
    violation = Violation.get(Violation.uuid == uuid)


    return render_template('detail.html', 
    street_address = violation.street_address, 
    county = violation.county, 
    site_name = violation.site_name,
    type = violation.media)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)