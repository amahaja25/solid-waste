import csv
import datetime
from flask import Flask, render_template, request, redirect, url_for
from peewee import *
app = Flask(__name__)

db = SqliteDatabase('solid_waste.db')
db.connect()

categories = {
    'hazardous-waste': 'SWP-Hazardous Waste',
    'refuse-disposal': 'SWP-Refuse Disposal',
}

class County(Model):
    slug = TextField(null=True)
    county = CharField()

    class Meta:
        table_name = "counties"
        database = db

class Violation(Model):
    site_no = CharField()
    site_name = CharField()
    street_address = CharField()
    city_state_zip = CharField()
    county = CharField()
    media = CharField()
    violation_date = DateField()
    status = CharField()
    resolved_date = DateField(null=True)  # Assuming resolved date can be null if unresolved
    uuid = CharField(primary_key=True, unique=True)

    @property
    def county_obj(self):
        return County.get(County.county == self.county)

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


@app.route("/category/<category_slug>")
def category(category_slug):
    template = 'category.html'

    category = categories[category_slug]
    
    violation_list = Violation.select().where(
        (Violation.media == category) 
    ).join(County, on=(Violation.county == County.county))

    hazardous_count = violation_list.count()

    return render_template(template, violation_list=violation_list, hazardous_count=hazardous_count, category=category)

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