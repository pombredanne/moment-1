Moment
======

A simple screen capture API based on PhantomJS, CasperJS, Redis, RQ, Flask, Gunicorn and good intentions...

We're just sitting on the shoulders of giants.

How to use
==========

Docs will come.

Examples
========

We have a demo install setup with a test user.

http://moment.prjts.com/

Here are the temporary credentials:

**username:** test_user
**key:** c413c0979c2c42bbbc1adb3c55797851
**token:** 6cdf4a492ecd4500ec80b6f4d95d0529

The current status of the code exposes a simple capture API - you pass a set of valid parameters, and you get back a file in return. Some parameters are required, and the rest have sensible defaults.

Required
++++++++

* user: the user's key
* token: the user's token
* url: the URL to capture

Optional
++++++++

* format: 'png' or 'pdf'. 'png' default.
* viewport: 'width,height'. '1280,800' default.
* and more to be documented.....
