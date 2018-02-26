Django Finalware
====================

**A utility application that offers the most commonly-used tools.**

[![build-status-image-travis]][travis]
[![build-status-image-fury]][fury]
[![build-status-image-pypi]][pypi]


Overview
====================

A utility application that offers the most commonly-used tools and mixins.


How to install
====================

    1. easy_install django-toolware
    2. pip install django-toolware
    3. git clone http://github.com/un33k/django-toolware
        a. cd django-toolware
        b. run python setup.py
    4. wget https://github.com/un33k/django-toolware/zipball/master
        a. unzip the downloaded file
        b. cd into django-toolware-* directory
        c. run python setup.py install


How to use
====================

   ```python

    # Add `toolware` to the very end of your INSTALLED_APPS

    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.humanize',
        'django.contrib.admin',

        # ......

        'toolware',
    ]


    # Have a look at the source code for the available utility tools and mixins
   ```


Running the tests
====================

To run the unit test:

    python manage.py test


License
====================

Released under a ([MIT](LICENSE)) license.


[build-status-image-travis]: https://secure.travis-ci.org/un33k/django-toolware.png?branch=master
[travis]: http://travis-ci.org/un33k/django-toolware?branch=master

[build-status-image-fury]: https://badge.fury.io/py/django-toolware.png
[fury]: http://badge.fury.io/py/django-toolware

[build-status-image-pypi]: https://pypip.in/d/django-toolware/badge.png
[pypi]: https://crate.io/packages/django-toolware?version=latest
