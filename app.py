import csv
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

def get_csv():
    csv_path = './static/solid_waste_violations.csv'
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

@app.route("/refuse-disposal")
def refuse():
    template = 'refuse.html'
    violation_list = get_csv()
    refuse_list = [violation for violation in violation_list if violation['media'] == 'SWP-Refuse Disposal']
    return render_template(template, refuse_list=refuse_list)
   

@app.route("/composting")
def composting():
    template = 'composting.html'
    violation_list = get_csv()
    composting_list = [violation for violation in violation_list if violation['media'] == 'SWP-Composting']
    return render_template(template, composting_list=composting_list)

@app.route("/hazardous-waste")
def hazard():
    template = 'hazard.html'
    violation_list = get_csv()
    hazard_list = [violation for violation in violation_list if violation['media'] == 'SWP-Hazardous Waste']
    return render_template(template, hazard_list=hazard_list)

@app.route("/sewage-sludge")
def sewage():
    template = 'sewage.html'
    violation_list = get_csv()
    sewage_list = [violation for violation in violation_list if violation['media'] == 'SWP-Sewage Sludge']
    return render_template(template, sewage_list=sewage_list)

@app.route("/balloon-release")
def balloon():
    template = 'balloon.html'
    violation_list = get_csv()
    balloon_list = [violation for violation in violation_list if violation['media'] == 'SWP-Balloon Release']
    return render_template(template, balloon_list=balloon_list)


@app.route("/scrap-tire")
def tire():
    template = 'tire.html'
    violation_list = get_csv()
    tire_list = [violation for violation in violation_list if violation['media'] == 'SWP-Scrap Tire']
    return render_template(template, tire_list=tire_list)


@app.route("/natural-wood-waste")
def wood():
    template = 'wood.html'
    violation_list = get_csv()
    wood_list = [violation for violation in violation_list if violation['media'] == 'SWP-Natural Wood Waste']
    return render_template(template, wood_list=wood_list)

@app.route("/surface-water-discharge")
def surface_water():
    template = 'surface_water.html'
    violation_list = get_csv()
    surface_water_list = [violation for violation in violation_list if violation['media'] == 'Surface Water Discharge Unauthorized']
    return render_template(template, surface_water_list=surface_water_list)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)