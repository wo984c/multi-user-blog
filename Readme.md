# Multi User Blog

Very simple multi-user blog where users post, comment, and even like other users posts. 

## Demo

For the live version click _[here](https://wo984c-mublog.appspot.com)._

## Quick Start
### Software Requirements
1. Python Version 2.7 -_[Beginners Guide](https://wiki.python.org/moin/BeginnersGuide/Download)_
2. Google App Engine SDK -_[Download the Cloud SDK URL](https://cloud.google.com/appengine/docs/standard/python/download)._

### Frameworks
* Bootstrap
* jQuery

### How to run the multi-user blog

_Clone the repo from github_
``` sh
# git clone https://github.com/wo984c/multi-user-blog.git
```
_Load the application locally_
``` sh
# dev_appserver.py .
```

_Go to http://localhost:8080/_

**Deploy the application to appspot.com (optional)**

_Login to gcloud_

``` sh
# gcloud auth login
```

_Create the project id [here](https://console.cloud.google.com/)_

_Deploy the app_

``` sh
# gcloud app deploy app.yaml --project <proj_id>
```

### License

Multi User Blog is released under the [MIT license](https://github.com/wo984c/multi-user-blog/LICENSE.txt).


