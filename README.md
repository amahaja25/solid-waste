[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=14703123)
# final-project

To deploy my news application, open a GitHub codespace and enter these two lines in the terminal:

```
pip install flask peewee geopy
python app.py
```

Then, click the little button on the popup that says "Open in Browser."
# Updates log
<b>7/21 update </b>
I used Leaflet + a simple script to incorporate locator maps on each site page. To do this, I had to geocode each address to get the lat and long, and to do that, I had to join two of the rows in the data to create a full address. I used Nominatim with geopy, and I think I probably hit the rate limit, because only some of the addresses are actually geocoded and therefore a lot of the sites just have gray boxes instead of functional maps. Going to see if there are alternatives that I could use like the Google Maps API or another option. I really, really like what the maps add to this app in being able to see where the sites are and particularly how big or small they are! 

<b>Final final project update 5/15 --</b>
This news app looks very different to what I had envisioned starting out. Because of that, I am a little disappointed with just how much I was unable to accomplish, but I still think I was able to create a product that does at least some of what I set out to achieve, which was to create something that displays the solid waste data in a better fashion than it currently is on the Maryland Department of the Environment website, and I think I did that! Even just the few paragraphs I added to each of the violation type pages give at least a little more context to what the data actually is and the significance of one of these violations, which is definitely a step up from the original site, in my opinion. My news app is just deployed within GitHub Codespaces right now, but I plan to put it on a GitHub pages site after this.

There are still so many ideas I think would make this news app much more useful than it currently is, and I am most disappointed that I didn’t end up getting very far with the pdfs. Even though we managed to get the pdfs on the first page using playwright, and I even did the OCR on the few I had and got text files, I could not figure out how to connect the pdfs I got to the csv I got with my scraper, and downloading them individually did not solve my problems as the names were formatted a little differently from downloading the pdfs versus getting them from playwright. If I had more time, I would have liked to figure it out, since the pdfs were the most valuable part of this data because they are essentially hidden right now — there is so much data just within the text that I could use in this news app, but I could not get to it before the submission date.

Another thing I really wish I had gotten to was using Leaflet to create little maps on each of the site pages to show where each violation site was. This was definitely something I could have done, since I would have just mainly had to figure out a way to geocode each of the locations, but again, I simply did not have enough time in the end.

I ultimately decided to pivot and focus on the data I already had, and there was still a lot for me to work with. I had a lot of trouble with the urls and using the logic in Flask to get the right links. Trying to get the dropdowns to work was especially frustrating, but creating a separate model for counties and manually entering each violation category got me two forms that do exactly what I want them to do, and I have pages for each county, violation type, site and individual violation. I also edited the violation type form a bit so it shows violation names that are easier to digest and read instead of the ones in the csv that are formatted with “SWP-” in front of the actual name. 

I think I did a fairly good job with the design of the news app itself! It has been a while since I’ve coded in HTML and CSS, but I think that even though my design is fairly simple, it is clean and visually appealing (at least to me). The tables ended up being more frustrating than they needed to be, because I had completely forgotten that DataTables existed and was trying to manually paginate my tables until I remembered at the last minute, which was incredibly helpful and made the tables look way better than whatever I was trying. I ended up using a y scroll in DataTables that was similar to the first news app example, and the little functional details like being able to sort and search make this news app more elevated as well. 

At one point, I realized that the violation date was formatted m/d/y but the resolved dates were d/m/y, and I fixed this by changing the format when I scrape the csv. I also realized that for many of these violations (even on the regular MDE website before I touched the data) the resolved date was earlier than the violation date. I had planned on making a resolved-violation date column to show the length it took to resolve, but because this was really weird I decided to not do that until I knew for sure why this was. A lot of information for this news app would be made easier if I had just talked to someone who actually works at the MDE, so I think if I email someone and ask some more questions about the data as well, the issue about the date and even understanding the violation type description would be fixed.

I really liked being able to search in the tables, and I was torn on whether I should do a big search just on my home page. I ultimately stuck with filtering, which still leads to the option of search later, and I think that works well. I might add a big search bar later on the home page, but due to there being more than 1,000 records, I didn’t want the search of everything to be overwhelming to sift through on the home page before some of the information is even explained, so going by county, site or violation type narrows it down at least a little before the search.

As long as the Department of the Environment continues to issue violations and update their data — which they currently do daily — my app will be maintained. I plan on deploying the app as a GitHub pages site soon so it doesn’t just live in a codespace, and if I do that, all of the code and the database itself will be readily available for users to look at in my repository. As time goes on, I would need to alter parts of how my app works. I would want to add something to account for the time element (which I also could not do now). If I have more than just 4 years of data, I could see how the number and types of violations change over time, and I would want to incorporate graphics in showing this. If new types of violations get added to this data, I need to figure out a way to have slugs for them without doing it manually, because it might not even be on my radar that there’s a new type in my data. My scraper and shell file are set up to run every day with GitHub Actions, and I will know if they don’t run because I get emails whenever they do not run. Even though the data is available for download on the MDE website, it will live on even if this app retires, and my scraper can continue to get the most updated versions of the solid waste violations. I want to play around with some of the things I wasn’t able to get done when I have more free time in the summer, so hopefully one day I will have created the news app I aimed to create when I started this project!




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
