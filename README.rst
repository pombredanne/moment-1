Moment
======

A simple screen capture API based on PhantomJS, CasperJS, Redis, RQ, Flask, Gunicorn and good intentions...

We're just sitting on the shoulders of giants.

Contributing
------------

Please help:

* Code_
* Issues_
* Demo_

The goal of Moment is a simple, easy to deploy and use, API for screen captures.

The feature set will remain minimal, and the code should be clean and highly readable.

We'd like to complete the following, and only the following, to be feature complete for V1:

* Expose RESTful API endpoints for users
* Create a UI for user accounts
* Implement a simple and elegant looking solution for watermarking images with their source URL and any license declaration
* Implement a proper backup and restore mechanism for the Redis database
* Implement image cropping
* Expose 'delay' and 'event' arguments for the capture method


Capturing
---------

We have a demo_ setup with a test user. Please make some test captures, and if you have any issues, please file a bug_.

Here are the temporary credentials:

* **username:** test_user
* **key:** c413c0979c2c42bbbc1adb3c55797851
* **token:** 6cdf4a492ecd4500ec80b6f4d95d0529

The current status of the code exposes a simple capture API - you pass a set of valid parameters, and you get back a file in return. Some parameters are required, and the rest have sensible defaults.

Required
++++++++

* **user:** the user's key
* **token:** the user's token
* **url:** the URL to capture

Optional
++++++++

* **format:** 'png' or 'pdf'. 'png' default.
* **viewport:** 'width,height'. '1280,800' default.
* **target:** 'element' or '#id' or '.class'. 'body' default.
* and more to be documented.....

**Note:**

If you need to use '?' or '#' symbols as values in the query - that is fine, just make sure they are encoded.

* ? : %3F
* # : %23

Examples
++++++++

Some example captures:

* `The Public Knowledge Workshop`_
* `Education Expenditure from Open Budget Comparator`_
* `Map Chart from the Google Charts Gallery`_
* `D3 Voronoi Tesselation`_
* `YouTube Featured Videos Section`_
* `Ynet (Israeli Tabloid)`_
* `Sydney Morning Herald (Australian Tabloid)`_


Setting up an instance
----------------------

* Make sure you have Python_, CasperJS_, PhantomJS_ and Redis_ available on your system
* Create a virtualenv called **moment**, in your preferred way
* Clone the repo into your project folder: e.g: ``git clone git@github.com:pwalsh/moment.git``.
* Install the pip-managed requirements: ``pip install -r -U requirements.txt``
* Run the server. You can run Flask's development server for debugging with: ``python dev.py`` from the project root. Alternatively, Run Gunicorn with ``gunicorn moment:app``
* Visit 127.0.0.1:9000 in your browser.
* Currently, only the /capture/ endpoint is implemented. This is a convenience endpoint that any user can hit with a set of parameters, and have a file returned. See examples above for how to construct a query to /capture.

.. _Python: http://python.org/download/releases/2.7.5/
.. _CasperJS: http://casperjs.org/
.. _PhantomJS: http://phantomjs.org/
.. _Redis: http://redis.io/
.. _bug: https://github.com/pwalsh/moment/issues?state=open
.. _demo: http://moment.prjts.com/
.. _Code: https://github.com/pwalsh/moment
.. _Issues: https://github.com/pwalsh/moment/issues?state=open
.. _Demo: http://moment.prjts.com/
.. _The Public Knowledge Workshop: http://moment.prjts.com/capture/?user=c413c0979c2c42bbbc1adb3c55797851&token=6cdf4a492ecd4500ec80b6f4d95d0529&url=http://www.hasadna.org.il/
.. _Education Expenditure from Open Budget Comparator: http://moment.prjts.com/capture/?user=c413c0979c2c42bbbc1adb3c55797851&token=6cdf4a492ecd4500ec80b6f4d95d0529&url=http://compare.open-budget.org.il/%3F00/0020&target=.frame
.. _Ynet (Israeli Tabloid): http://moment.prjts.com/capture/?user=c413c0979c2c42bbbc1adb3c55797851&token=6cdf4a492ecd4500ec80b6f4d95d0529&url=http://www.ynet.co.il/
.. _Map Chart from the Google Charts Gallery: http://moment.prjts.com/capture/?user=c413c0979c2c42bbbc1adb3c55797851&token=6cdf4a492ecd4500ec80b6f4d95d0529&url=https://google-developers.appspot.com/chart/interactive/docs/gallery/geochart%23Example&target=.framebox
.. _D3 Voronoi Tesselation: http://moment.prjts.com/capture/?user=c413c0979c2c42bbbc1adb3c55797851&token=6cdf4a492ecd4500ec80b6f4d95d0529&url=http://bl.ocks.org/mbostock/4060366&target=iframe
.. _YouTube Featured Videos Section: http://moment.prjts.com/capture/?user=c413c0979c2c42bbbc1adb3c55797851&token=6cdf4a492ecd4500ec80b6f4d95d0529&url=http://www.youtube.com/&target=.lohp-newspaper-shelf
.. _Sydney Morning Herald (Australian Tabloid): http://moment.prjts.com/capture/?user=c413c0979c2c42bbbc1adb3c55797851&token=6cdf4a492ecd4500ec80b6f4d95d0529&url=http://www.smh.com.au


