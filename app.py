# going to do the baseline stuff from the news app tutorial with flask so i at least have something to start out with.
import datetime
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

    total_count = Violation.select().count()
    
    refuse_count = Violation.select().where(
        (Violation.media == 'SWP-Refuse Disposal') 
    ).count()

    hazardous_count = Violation.select().where(
        (Violation.media == 'SWP-Hazardous Waste') 
    ).count()

    tire_count = Violation.select().where(
        (Violation.media == 'SWP-Scrap Tire') 
    ).count()

    wood_count = Violation.select().where(
        (Violation.media == 'SWP-Natural Wood Waste') 
    ).count()

    compost_count = Violation.select().where(
        (Violation.media == 'SWP-Composting') 
    ).count()

    sewage_count = Violation.select().where(
        (Violation.media == 'SWP-Sewage Sludge') 
    ).count()

    balloon_count = Violation.select().where(
        (Violation.media == 'SWP-Balloon Release') 
    ).count()

    surface_water_count = Violation.select().where(
        (Violation.media == 'Surface Water Discharge Unauthorized') 
    ).count()

    template = 'index.html'
    return render_template(template,
    refuse_count = refuse_count,
    hazardous_count = hazardous_count,
    tire_count = tire_count,
    wood_count = wood_count,
    compost_count = compost_count,
    sewage_count = sewage_count,
    balloon_count = balloon_count,
    surface_water_count = surface_water_count,
    total_count = total_count
    )

@app.route("/violation/<uuid>")
def detail(uuid):
    template = 'detail.html'
    violation = Violation.get(Violation.uuid == uuid)
    
    violation_date = datetime.datetime.strptime(violation.violation_date, '%m/%d/%Y')
    date_start = violation_date.strftime('%B %d, %Y')

    return render_template('detail.html', 
    street_address = violation.street_address, 
    county = violation.county, 
    site_name = violation.site_name,
    type = violation.media,
    date_start = date_start,
    violation_type = violation.media)

@app.route("/refuse-disposal")
def refuse():
    template = 'refuse.html'
    return render_template(template)

@app.route("/composting")
def composting():
    template = 'composting.html'
    return render_template(template)

@app.route("/hazardous-waste")
def hazard():
    template = 'hazard.html'
    return render_template(template)

@app.route("/sewage-sludge")
def sewage():
    template = 'sewage.html'
    return render_template(template)

@app.route("/balloon-release")
def balloon():
    template = 'balloon.html'
    return render_template(template)

@app.route("/scrap-tire")
def tire():
    template = 'tire.html'
    return render_template(template)

@app.route("/natural-wood-waste")
def wood():
    template = 'wood.html'
    return render_template(template)

@app.route("/surface-water-discharge")
def surface_water():
    template = 'surface_water.html'
    return render_template(template)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)