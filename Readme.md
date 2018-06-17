# PROJECT: Multi User Blog

Very simple multi-user blog where users post content, comment on other users posts, and like other users' posts. Login is required in order to be able to submit a post or comment. Only the author of the post or comment has the right to edit or delete content. The author can't like his/her own post.



## Quick Start
### Software Requirements
1. Python Version 2.7 - Refer to the [Beginners Guide](https://wiki.python.org/moin/BeginnersGuide/Download) for installation instructions
2. Google App Engine SDK - Refer to [Download the Cloud SDK URL](https://cloud.google.com/appengine/docs/standard/python/download)


### What is included

Within the download you'll find the following files:

* model.py - data models
* helper.py - helper functions
* handler.py - handler class
* blog.py - application code
* app.yaml - app settings
* templates directory - html templates
* static directory - java scripts, css, fonts, and images 
* README.md - this readme file

### How to run the multi-user blog

Clone the repo from github by running
``` sh
git clone https://github.com/wo984c/multi-user-blog.git

```
Load the application by running
``` sh
dev_appserver.py .

```
For the live version click [here](https://wo984c-mublog.appspot.com)

### Implemented Features

* Front page lists blog posts
* Posts have their own page
* Form for user registration
* Form to submit new entries
* Set Cookie on login
* Destroy cookie on logout
* Only the author can edit or delete his/her post or comment
* Can't like your own post
* Users can comment on posts
