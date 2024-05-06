import csv
import datetime
from flask import Flask, render_template, request, redirect, url_for
from peewee import *
app = Flask(__name__)

db = SqliteDatabase('solid_waste.db')
db.connect()

class County(Model):
    slug = TextField(null=True)
    name = CharField()

    class Meta:
        table_name = "counties"
        database = db

class Violation(Model):
    site_no = CharField()
    site_name = CharField()
    street_address = CharField()
    city_state_zip = CharField()
    county = ForeignKeyField(County, backref='violations', field='name')  # Establishing foreign key relationship
    media = CharField()
    violation_date = DateField()
    status = CharField()
    resolved_date = DateField(null=True)  # Assuming resolved date can be null if unresolved
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

    counties = County.select()
    print(counties)

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
    total_count = total_count,
    counties=counties
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

@app.route("/site/<site_no>")
def site(site_no):
    template = 'site.html'

    site_number = Violation.get(Violation.site_no == site_no)
    return render_template(template,
    site_name = site_number.site_name,
    street_address = site_number.street_address,
    county = site_number.county,
    city_state_zip = site_number.city_state_zip
    )


def get_csv():
    csv_path = './static/solid_waste_violations.csv'
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    csv_list = list(csv_obj)
    return csv_list

@app.route("/refuse-disposal")
def refuse():
    template = 'refuse.html'
    page = request.args.get('page', 1, type=int)
    per_page = 50

    refuse_count = Violation.select().where(
        (Violation.media == 'SWP-Refuse Disposal') 
    ).count()

    violation_list = get_csv()
    refuse_list = [v for v in violation_list if v['media'] == 'SWP-Refuse Disposal']  # Filter data
    refuse_count = len(refuse_list)

    refuse_paginated = refuse_list[(page - 1) * per_page : page * per_page]

    total_pages = (refuse_count + per_page - 1) // per_page  # Calculate total number of pages
    return render_template('refuse.html', refuse_list=refuse_paginated, refuse_count=refuse_count, page=page, total_pages=total_pages)
    
   

@app.route("/composting")
def composting():
    template = 'composting.html'

    compost_count = Violation.select().where(
        (Violation.media == 'SWP-Composting') 
    ).count()

    violation_list = get_csv()
    composting_list = [violation for violation in violation_list if violation['media'] == 'SWP-Composting']
    return render_template(template, composting_list=composting_list, compost_count=compost_count)

@app.route("/hazardous-waste")
def hazard():
    template = 'hazard.html'

    violation_list = Violation.select().where(
        (Violation.media == 'SWP-Hazardous Waste') 
    )

    hazardous_count = len(violation_list)

    return render_template(template, hazard_list=violation_list, hazardous_count=hazardous_count, counties=counties)

@app.route("/sewage-sludge")
def sewage():
    template = 'sewage.html'

    sewage_count = Violation.select().where(
        (Violation.media == 'SWP-Sewage Sludge') 
    ).count()

    violation_list = get_csv()
    sewage_list = [violation for violation in violation_list if violation['media'] == 'SWP-Sewage Sludge']
    return render_template(template, sewage_list=sewage_list, sewage_count=sewage_count)

@app.route("/balloon-release")
def balloon():
    template = 'balloon.html'

    balloon_count = Violation.select().where(
        (Violation.media == 'SWP-Balloon Release') 
    ).count()

    violation_list = get_csv()
    balloon_list = [violation for violation in violation_list if violation['media'] == 'SWP-Balloon Release']
    return render_template(template, balloon_list=balloon_list,balloon_count=balloon_count)


@app.route("/scrap-tire")
def tire():
    template = 'tire.html'

    tire_count = Violation.select().where(
        (Violation.media == 'SWP-Scrap Tire') 
    ).count()

    violation_list = get_csv()
    tire_list = [violation for violation in violation_list if violation['media'] == 'SWP-Scrap Tire']
    return render_template(template, tire_list=tire_list, tire_count=tire_count)


@app.route("/natural-wood-waste")
def wood():
    template = 'wood.html'

    wood_count = Violation.select().where(
        (Violation.media == 'SWP-Natural Wood Waste') 
    ).count()

    violation_list = get_csv()
    wood_list = [violation for violation in violation_list if violation['media'] == 'SWP-Natural Wood Waste']
    return render_template(template, wood_list=wood_list, wood_count=wood_count)

@app.route("/surface-water-discharge")
def surface_water():
    template = 'surface_water.html'

    surface_water_count = Violation.select().where(
        (Violation.media == 'Surface Water Discharge Unauthorized') 
    ).count()

    violation_list = get_csv()
    surface_water_list = [violation for violation in violation_list if violation['media'] == 'Surface Water Discharge Unauthorized']
    return render_template(template, surface_water_list=surface_water_list, surface_water_count=surface_water_count)

@app.route("/redirect", methods=["POST"])
def redirect_to_county():
    slug = request.form.get('slug')
    print("slug:", slug)
    return redirect(url_for("county", slug=slug))

# Route for displaying jurisdiction details
@app.route("/county/<slug>")
def county(slug):
    county = County.get(County.slug == slug)
    county_total_count = Violation.select().where(
        (Violation.county == county.county)).count()

    return render_template('county.html', county=county, county_total_count=county_total_count)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)