rm -f solid_waste.db
pip install sqlite-utils datasette
sqlite-utils insert solid_waste.db violations static/solid_waste_violations.csv --csv
sqlite-utils insert solid_waste.db counties static/jurisdictions.csv --csv