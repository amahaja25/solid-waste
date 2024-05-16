from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from peewee import *
app = Flask(__name__)

db = SqliteDatabase('solid_waste.db')
db.connect()

categories = {
    'hazardous-waste': ('SWP-Hazardous Waste', 'Hazardous Waste'),
    'refuse-disposal': ('SWP-Refuse Disposal', 'Refuse Disposal'),
    'scrap-tire': ('SWP-Scrap Tire', 'Scrap Tire'),
    'wood-waste': ('SWP-Natural Wood Waste', 'Natural Wood Waste'),
    'composting': ('SWP-Composting', 'Composting'),
    'sewage': ('SWP-Sewage Sludge', 'Sewage Sludge'),
    'balloon': ('SWP-Balloon Release', 'Balloon Release'),
    'surface-water': ('Surface Water Discharge Unauthorized', 'Unauthorized Surface Water Discharge')
    }

categories_description = {
    'balloon': 'According to a Maryland law passed in the 2021 legislative session, people may not intentionally release a balloon into the atmosphere or participate in mass balloon releases, which consist of 10 or more balloons being released into the atmosphere. <br><br> Exceptions include unintentionally released balloons and balloons released for meteorological or official scientific research purposes.',
    'wood-waste': 'According to the MDE, natural wood waste generally occurs when land is cleared for construction. This type of waste consists of discarded vegetation “in its natural state.” <br><br> Natural wood waste has to be disposed of in specific Natural Wood Waste Recycling Facilities, which process tree stumps, logs and limbs. The facilities make mulch and compost out of the wood waste and distribute or sell it afterwards, according to the MDE.',
    'hazardous-waste': 'Hazardous waste is any substance that threatens to harm human health or the environment or has the potential to “cause or contribute to an increase in mortality or serious illness,” according to the MDE. <br><br> This form of waste must be shipped to a specific hazardous waste facility that accepts it, but if a person has the appropriate permit, they may treat it themself. MDE inspectors routinely inspect hazardous waste generators and facilities unannounced. Household waste is not regulated as hazardous waste.',
    'composting': 'The MDE issues permits that are necessary to construct or operate a composting facility in the state, according to Maryland law. Exemptions are applicable in instances such as residential composting, composting sites that are less than 5,000 square feet or facilities that are managed by the government and compost animal carcasses as part of maintenance activities.<br><br>Composting facilities should not create disruptive odors or air pollution, harm the environment, lead to insect, rodent or animal infestations, leak pollutants to state waters or generally create hazards to public health and safety, according to the MDE.',
    'scrap-tire': 'Illegal stockpiles of scrap tires, which are tires that are no longer suitable for their original purpose, can lead to fire hazards, become breeding grounds for mosquitoes or disease-carrying agents and are “unsightly,” according to MDE’s website. <br><br>According to the Maryland Code of the Environment, people may only dispose of scrap tires through approved facilities or licensed scrap tire haulers.',
    'sewage': 'Sewage sludge — also known as biosolids — is the semi-solid residue that is produced when sewage or wastewater is treated and decontaminated. <br><br> According to Maryland law, people are not allowed to transport, compost, dispose or use sewage sludge unless they have a Sewage Sludge Utilization Permit from MDE.',
    'refuse-disposal': 'According to Maryland law, anyone who installs, alters or uses a refuse disposal system is required to have a permit. These facilities include municipal, rubble, industrial waste, and land clearing debris landfills as well as incinerators, processing facilities and transfer stations.',
    'surface-water': 'Industrial facilities that release wastewater or stormwater into Maryland surface waters such as  lakes, creeks, streams, rivers, reservoirs and the ocean, are required to have permits from the MDE to do so. The permit makes sure that the discharge meets Maryland water quality standards.'
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
    violation_date = DateTimeField()
    status = CharField()
    resolved_date = DateTimeField()
    violation = CharField()
    id = CharField(primary_key=True, unique=True)

    @property
    def county_obj(self):
        return County.get(County.county == self.county)

    class Meta:
        table_name = "violations"
        database = db



@app.route("/")
def index():

    total_count = Violation.select().count()

    counties = County.select()

    most_violations = (Violation.select(Violation.county, fn.COUNT(Violation.county).alias('count')).group_by(Violation.county).order_by(fn.COUNT(Violation.county).desc())
                       .limit(1))
    most_violations_county = most_violations.get()
    most_violations_info = {
        'county': most_violations_county.county,
        'count': most_violations_county.count
        }

    most_common_violation = (Violation
                             .select(Violation.media, fn.COUNT(Violation.media).alias('count'))
                             .group_by(Violation.media)
                             .order_by(fn.COUNT(Violation.media).desc())
                             .limit(1))
    
    most_common = most_common_violation.get()
    violation_name = categories[most_common.media][1] if most_common.media in categories else most_common.media

    most_common_info = {
        'type': violation_name,
        'count': most_common.count
    }

    site_with_most_violations = (
        Violation
        .select(Violation.site_no, Violation.site_name, fn.COUNT(Violation.site_no).alias('count'))
        .group_by(Violation.site_no, Violation.site_name)
        .order_by(fn.COUNT(Violation.site_no).desc())
        .limit(1)
        .get()
    )
    
    site_with_most_violations_info = {
        'site_no': site_with_most_violations.site_no,
        'site_name': site_with_most_violations.site_name,
        'count': site_with_most_violations.count
    }

    template = 'index.html'
    return render_template(template,
    total_count = total_count,
    counties=counties,
    categories=categories,
    most_violations=most_violations_info,
    most_common=most_common_info,
    violation_name=violation_name,
    site_with_most_violations=site_with_most_violations_info
    )


@app.route("/violation/<id>")
def detail(id):
    template = 'detail.html'
    violation = Violation.get(Violation.id == id)

    if violation.violation_date:
        date_start = datetime.strptime(violation.violation_date, "%Y/%m/%d").strftime('%B %d, %Y')
    else:
        date_start = 'Unknown'

    
    other_violation_count = Violation.select().where(Violation.site_no == violation.site_no).count() - 1


    return render_template('detail.html', 
                           street_address=violation.street_address, 
                           county=violation.county, 
                           site_name=violation.site_name,
                           date_start=date_start,
                           violation_type=violation.media,
                           violation=violation,
                           other_violation_count=other_violation_count)  

@app.route("/site/<site_no>")
def site(site_no):
    template = 'site.html'

    site_number = Violation.get(Violation.site_no == site_no)

    total_violations = (Violation
                        .select()
                        .where(Violation.site_no == site_no)  
                        .count())
    

    violation_list = Violation.select().where(
        Violation.site_no == site_no
    ).order_by(Violation.violation_date.desc())

    site_violation_count = violation_list.count()

    return render_template(template,
    site_name = site_number.site_name,
    street_address = site_number.street_address,
    county = site_number.county,
    city_state_zip = site_number.city_state_zip,
    violation_list = violation_list,
    site_violation_count = site_violation_count,
    )

@app.route("/redirect-to-county", methods=["POST"])
def redirect_to_county():
    slug = request.form.get('slug')
    print("slug:", slug)
    return redirect(url_for("county", slug=slug))

@app.route("/county/<slug>")
def county(slug):
    county = County.get(County.slug == slug)
    county_total_count = Violation.select().where(Violation.county == county.county).count()



    total_violations = (Violation
                        .select()
                        .where(Violation.county == county.county)   
                        .count())
    
    

    violation_list = Violation.select().where(
        Violation.county == county.county
    ).order_by(Violation.violation_date.desc())


    most_violations_site = (
        Violation
        .select(Violation.site_no, Violation.site_name, fn.COUNT(Violation.site_no).alias('count'))
        .where(Violation.county == county.county)
        .group_by(Violation.site_no, Violation.site_name)
        .order_by(fn.COUNT(Violation.site_no).desc())
        .limit(1)
        .get()
    )
    
    most_violations_info = {
        'site_no': most_violations_site.site_no,
        'site_name': most_violations_site.site_name,
        'count': most_violations_site.count
    }


    return render_template('county.html', county=county, county_total_count=county_total_count, violation_list = violation_list,most_violations_info=most_violations_info)

@app.route("/redirect-to-category", methods=["POST"])
def redirect_to_category():
    category_slug = request.form.get('category_slug')
    return redirect(url_for("category", category_slug=category_slug))

@app.route("/category/<category_slug>")
def category(category_slug):
    template = 'category.html'

    category = categories[category_slug][0]
    description = categories_description.get(category_slug)



    total_violations = (Violation
                        .select()
                        .where(Violation.media == category)
                        .join(County, on=(Violation.county == County.county))
                        .count())

    



    violation_list = (Violation
                      .select()
                      .where(Violation.media == category)
                      .join(County, on=(Violation.county == County.county))
 )

    

    hazardous_count = violation_list.count()

    

    return render_template('category.html', violation_list=violation_list, hazardous_count=hazardous_count,
                           description=description, category=category)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)