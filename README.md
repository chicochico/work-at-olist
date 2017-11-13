# Work at Olist

[![Build Status](https://travis-ci.org/chicochico/work-at-olist.svg?branch=master)](https://travis-ci.org/chicochico/work-at-olist)
[![Code Health](https://landscape.io/github/chicochico/work-at-olist/master/landscape.svg?style=flat)](https://landscape.io/github/chicochico/work-at-olist/master)


This is my solution for the chalenge proposed by Olist.

## API
The api provide the following endpoints:

- List all channels
- Channel detail with all categories of the channel
- Category detail
- Search channels names with keyword
- Search categories with keyword, lists all categories with keyword

Checkout the API documentation and running demo [here](https://young-garden-16956.herokuapp.com/api/v1/docs/).


## Solution

To store the data provided by the api a tree structure was used. A tree structure is well suited to represent hierarchical data.

The tree structure is stored in the database using MPTT (Modified Preorder Tree Transversal) algorithm, which allows fast reads, at the expense of slower inserts, since each node in the subtree need to have the left and right values updated when inserting. On the other hand, the left and right value gives the advantage of retrieving whole trees with single queries. For more information on MPTT check out [this](https://www.sitepoint.com/hierarchical-data-database/) article.

Each channel is a tree, the root represent the channel, and the descendants the categories. It is a forest.

Test data was taken from Google products taxonomy avaliable [here](https://support.google.com/merchants/answer/6324436?hl=en), the data was processed with Python in Jupyter notebook to generate csv files with random entries from the dataset. Checkout the repository [here](https://github.com/chicochico/categories).


## Command

A management command is provided to add data to a channel, the channel categories are dropped and updated with the new ones in the file provided.


### Usage
```
usage: manage.py importcategories [-h] [--version] [-v {0,1,2,3}]
                                  [--settings SETTINGS]
                                  [--pythonpath PYTHONPATH] [--traceback]
                                  [--no-color] [--sep SEPARATOR]
                                  channel file

Add categories from comma separated file to channel.

positional arguments:
  channel               Name for the channel.
  file                  File location.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        "myproject.settings.main". If this isn't provided, the
                        DJANGO_SETTINGS_MODULE environment variable will be
                        used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        "/home/djangoprojects/myproject".
  --traceback           Raise on CommandError exceptions
  --no-color            Don't colorize the command output.
  --sep SEPARATOR       Specify the separator used in the input file default
                        is (;).
```

Semicolon (;) is used as default separator, as the categories can have commas (,) themselves.

### Running the app

1. Clone this repo
2. Create a virtualenv
3. export DJANGO_SETTINGS_MODULE=work_at_olist.settings.dev
4. run ./manage.py migrate
5. run ./manage.py runserver
6. access localhost:8000 in your browser

#### Note

If deploying with production settings you have to set the following environment variables

1. DB_HOST the host of your database.
2. DB_NAME the name of your database.
3. DB_PASSWORD database access password..
4. DB_PORT database port.
5. DB_USER database user.
6. DJANGO_SETTINGS_MODULE work_at_olist.settings.prod or your own custom setting file.
7. SECRET_KEY the secret key.

If creating your own setting file, you can add the settings in the file instead of setting them into environment variables. Here they are set up this way to avoid putting sensitive information on version control.

## Tools

- Django web framework.
- Django-REST framework to build endpoints.
- Django-MPTT MPTT implementation for Django.
- Django-extensions provides many usefull manage commands.
- Jupyter notebook used to process testing data, and make interactions with the django app.
- Neovim text editor.
- iTerm terminal emulator for MacOS.
- DevDocs APIs and programming languages documentation search with instant results and fuzzy search.
- Heroku to host the demo app.
- Travis continuous integration, run tests and if tests passes deploy app to Heroku (only the master branch).

