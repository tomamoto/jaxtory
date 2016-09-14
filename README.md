# Jaxtory
## Let's tell a story together

Jaxtory is something simple I whipped up to help my lovely wife Jaxxy easily keep track of her chose-your-own adventure stories.  I am open to contributions, but not expecting this to draw a ton of widespread attention since setting it up requires so me advanced knowledge and might not be possible with the shared hosting (i.e. cPanel) that most artists are more familiar with.  Still, for those with the technical knowledge and resources required (like root shell access to their server/VPS), I'm creating some documentation to assist with those who really want to use this for themselves.  

### Dependencies
* **MongoDB** - Run `sudo apt-get install mongodb` or whatever is appropriate for your OS/Distro.
* **nginx** *(optional)* for reverse proxy in front of CherryPy - Run `sudo apt-get install nginx` or whatever is appropriate for your OS/Distro.

##### Python Modules
This project depends on the following modules:
* **cherrypy** - for our actual web front-end
* **pymongo** - to connect to and manipulate our database
* **imgurpython** - for imgur integration
* **jinja2** -templating engine
The simples way to install them is using pip with the following command:

```pip install cherrypy pymongo imgurpython jinja2
```
Or if root permission are necessary:
  ```sudo pip install cherrypy pymongo imgurpython jinja2`
  ```
### Usage

#### Initial Setup

You'll need to copy `config.py.example` into a file called `config.py` and fill in the necessary fields. USERS is where you set up credentials for accessing the admin interface.  A number of the remaining fields are related to the Imgur API that we're going to be using to actually host our images (and save lots of bandwidth in the process).  To get more information on the imgur API and create your account and get your app credentials, go [here](http://api.imgur.com/).

#### Starting the application:
Once your config.py is setup, you can start the app by simply running `./jaxtory_web.py` from the root of the app directory.

This will bring the server up and listen on the interface and port as defined in `server.conf`.  At this point, you should be able to hit your host with a web browser at the port you chose (i.e. `http://localhost:9098`) and see some sort of output, though if you haven't set anything up in admin, you won't see a whole heck of a lot.  You might even get an error message.

#### Accessing/using the admin interface

Go to the your base appl URL with the addition of **/admin** (i.e. `http://localhost:9098/admin`).  You will be prompted for a login.  This will be the username and password your set up in your config.py as *USERS*.  One inside, you should create a story using the forms and set it as your default (only the default story is visible to your users on the main part of the site).  Then click on the story link and you will be able to create you paging by uploading the associated images and definining the associated data like the description.  
**NOTE:**  The order of the pages is determined entirely by the Name which is sorted automatically in alphabetical order.  I recommended just using numbers like 001, 002, 003, etc. for your page names to keep them in order.  You can edit these data fields at any time after creation by clicking the `edit` button next to the page in question and then clicking `save` to immediately commit those changes.  You can delete a page (or story) at any time by clicking the **X** next to that particular item.

#### Accessing the app itself

Once a story and pages are setup as described above, your viewers should be able to view your properly configured default story at your base url (i.e. `http://localhost:9098`)
