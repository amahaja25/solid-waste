[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=14703123)
# final-project

To use:

pip install flask peewee

<strong>4/13</strong> --
For my final project, I want to make a news app that displays data about solid waste violations in Maryland based on data from Maryland's Open Data Portal. Maryland's website should be updated each day, so that means my news app should keep up with the most recent violations and be updated everyday. One record would be one of the violations, which is one row in the csv. The updates would be done incrementally as the data source gets updates over time.

I think the hardest part will be getting the text from the pdfs using tesseract. Getting the actual data isn't very hard as it is already available for me to export and is structured in the way I want it, so I won't be spending so much time figuring out how to scrape it. But I do want to figure out how to make the text of the violations searchable, because I think that would be the most useful part of this app. The purpose of this news app is to show not just the violations, but to also inform users about the laws/regulations that frequently get violated. The pdfs have the actual codes that were violated in each violation, so I wonder if there's something I can do with that information to incorporate it into my news app.

I don't think I want to make any part of this data not searchable. Earlier, I did think about narrowing down the news app to focus on certain violations rather than others, such just focusing on hazardous waste violations, but I think having all of the violation types would be better since they are all parts of the larger solid waste program in Maryland, so it makes sense to keep them all together. I want each violation to go to its own page, and I was also thinking about having each type of violation have its own page so I could provide additional context on what they mean. Based on the data, there are eight solid waste program categories, so maybe a page for each of those? The home page would display the sections and then each of the eight violation pages would display just the filtered data for that criteria is something I want to do. 

4/20 
* I got the csv from the website and cleaned the header names using pandas
* I used uuid to create unique id column for each violation. i did this so i can have a different url for each of the violations so each has its own page, there isnt a distinguishing value otherwise in the data
* got basic index and detail (individual violation) pages
* I wasn't able to get as much done as I wanted to but here is what my next steps are:
    * fix individual violation pages
    * build more detailed pages
    * create pages for each "group" of violations
    * make it so updating the csv and pulling it from the export link on the website is scheduled regularly
    * get all of the pdfs
    * OCR on pdfs