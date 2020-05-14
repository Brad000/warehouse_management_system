# Milestone Project 3 - Data Centric 
Data Centric Development Project - Code Institute 

### What The Project Acheive's 
---
The site is a warehouse management system that would be purchased and implemented in a storage company to handle and control their stock intake, movement and archvie. It is built using skills i have learnt to build a Flask framework website / application, the project also uses a MongoDB backend to store the data. Users can create, view, update and archive / delete data from the application in various forms which would aid the companies production and stock security. 

### Demo 
---
The site can be accessed using the link here https://wms-project1.herokuapp.com/ 

### UX 
--- 
#### Wireframe 
The wireframes for the intial design of the site can be found in the static file in the github respository. The design and flow of the application evolved as the site came to life, from an on paper drawing through the balsamiq tool. 

#### User Stories 
<em>As the business owner i would want my stock to be stored securely and so it is easily accessable.</em>
- Stock to be stored on a database itemized by unique customer codes and descriptions. 

<em>As the admin assistant i want the stock easily accessable with all the tools on hand to control the flow of the stock.</em>
- Search function which filters out results and shows relevant information, also gathers all functionality in one place to allow ease of use. 

<em>As the admin assistant i want a area to store the active product information for our inventory.</em>
- Stock cards to be built in that show all basic product information. 

<em>As the warehouse manager i want the warehouse operatives to be able to recipt goods onto the system but the process to be simple so it can be achieved by anyone in a efficient time.</em>
- A simple warehouse operative view will show only the required fields needed to perform relevant tasks. 

<em>As the business owner i want certain fields i.e delete only accessbale to managers.</em>
- Certain fields and functions will be only visable to certain user types. 

#### UX design
The site was created simple in design this is down to the application targeted at the storage & distrbution industires, i felt the simple design would lend to it being accessable and useable to all employees throughout a business. Keeping the design simple would avoid intimidating less tech savvy employees, rather than an over complicated site which didn't fit the intended purpose. 

The initial landing page lends to the business supplying the application with brief introduction and a link (to a dummy site), the login and register is clearly visable to move further into the application. 

The colour scheme for the site was set to lift the information from the page and make it easily visable the button colours transition through the site with icons to give a visual stimulus to the intent of the button. 

The site was built using Materialize as i had used Bootstrap in previous projects and wanted to ustilise another framework. 

The flow of the site works well and allows users to flow freely through all aspects of the site and the buttons and searches work well and as intended. 

#### Side Note! 
<strong>On building i had a issue with the CSS not loading all the classes i had built into the style.css file, mainly font color. I tried all routes to fix this including !important but they did not seem to load. to complete the project i utilized the materialze built in color classes. As i realize this is not the optimum method to style it was in neccesity rather than lack of knowledge.</strong> 

### Technologies Used
---
1. HTML
2. CSS 
3. Jquery (3.4.1)
4. Materialize (1.0.0)
5. MongoDB
6. Flask 
7. WTforms 

### Features
---
* The register and login page is a simple form using Wtforms. To register users fill out basic information. Username, password, email and usertype. The usertype will define later what views or functionality that user will have access too. 
* Once a user has logged onto the system, they are greated with the home page, this now shows the menu in the top left corner and a contact service for the application creator and a view for most recent app updates. (these are for design purpose only)
* The menu is a side nav which jumps out to the side once the icon is clicked, it shows through all the features needed to run the functionality of the application (this view differs between the manager / admin and the warehouse usertypes)
* The goods received page allows all users to receipt goods into the warehouse it is set as a form which requires all fields to be accessed before it will submit. The product code will only show products currently active on the system. (This is the only view available to the warehouse usertype)
* Stock control allows to search stock that is active on the system. the search field takes product code or delivery ref as a parameter. once a successful search is submitted the results show in the below the search field. from here the user can edit, relocate, dispatch or clear the search. 
* The edit, relocate and dispatch pages allow the user to perform different functionality using the same form format as the goods receipt. Edit allows for a full edit of all fields, Relocate is put in place to allow a quick movement of stock within the warehouse (only the location field is active in this view). The dispatch allows a user to dispatch goods from the system, this view has a dispatch date field in replace of the goods received date. (only the dispatch date is active in this view).
* The stock archive allows users to search the stock that has been dispatched from the system, if usertype is admin this will only show a view of the stock information that is dispatched. If the usertype is manager there will be a function to fully delete data from the system in case of error etc. On submitting the delete it will prompt a second check to avoid miss clicks and deleting stock in error. 
* The stock card views are very similar to the stock views. The stock cards are built to hold information on each active product on the system and allows for only current stock to be seleceted on reciept and also lends this information to the stock search fields. The stock cards can be created, edited, archived and deleted fully from the system. The functionality of this is the same as the stock. Where the admin has the access to all the functionality exept to fully delete data from the system, this is reserved for managers only. 
* Although i feel the site is intuative and allows users to move around it without lesson, to operate any application that is specific for a business / sector of industy a certain level of company knowledge is needed to operate these systems, this runs true with this application. 
* To access each individual usertype i have programmed default users for easy access 
    1. Username - manager 
       Password - manager1 
       Usertype - manager 
    2. Username - admin
       Password - admin123
       Usertype - admin 
    3. Username - warehouse
       Password - warehouse1
       Usertype - warehouse operative 

### Testing 
---
Throughout the build I have tested all functionality fully at each stage to ensure it functions correctly, All the links have been tested and direct you in the intended direction, links to external sources open in a new tab by using ```target="_blank"``` 

I ran the code through online validators and any minor issues where corrected. 

All the flash messages responded how they should and have been tested at various points. 

The creation, read, update and delete functions of the data were all tested at various stages and responded correctly. 

To initially check the connection between my data bases and build was successful i ran the following code: 

``` 
def mongo_connect(url):
   try: 
        conn=pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn 
    except: pymongo.errors.connectionfailure as e: 
        print("Could not connect to MongoDB: %e") %e 

conn = mongo_connect(MONGO_URI)

coll = conn[DBS_NAME][CONNECTION_NAME]

documents = coll.find()

for doc in documents:
    print(doc)
```
This allowed me to test in the terminal to access data from the database and confirm connection between the two. 

Whilst building the search function i followed the MongoDB documentation to build the search to allow users to type in any case (Lower / Upper) and find results even though the data is stored in UPPER case. the MongoDB doumentation advised to using ``` options i ``` the the query, this however did not run through as jinja advised options could not be used. 

I worked around this by asking python to ignore case in the code line below

``` {'product_desc': re.compile(orig_query, re.IGNORECASE)}, ``` 

Browser Testing: 

* Chrome 
* Firefox 
* Safari 
* Internet Explorer 

Device Testing: 

* Pixel 4 
* Iphone X, 11, 6, 7 
* Ipad 
* Android Tablet

On testing the goods reciept forms did not render correctly on mobile devices i amended this to allow each form line to occupy the entire row (s12) this corrected the issue. 

### Deployment 
--- 
Website was built in GitPod with the template supplied straight from github. version control was sent frequently through to github. 

My database (MongoDB) was set up within the Mongo web page. The database information is kept in a enviromental variable. (env.py), this is communicated across to the main python file using 

```
from os import path
import bcrypt
if path.exists("env.py"):
    import env
```

The application is deployed through Heroku,i connected my github page directly to the my heroku page to auto deploy any recent push to the master branch, due to the frequency of the deposits into the respository i hit a limit on deployed files. in this instance i deployed manually from the terminal. 

The Procfile and requirements.txt files allow heroku to get the application up and running. 

### Credits 
--- 
#### Content 
All the HTML and style.css content was written by me 
All the python file content was written by me 

The Jquery and layout of the site was taken from the materialze framework

#### Acknowledgements 
I discussed the use of WTforms with my mentor during reviews and he directed me to view there application within a project, i based my register and login forms from this. 



