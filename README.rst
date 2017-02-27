=====================
ACCEL IDSR Input Form
=====================
Installation
------------

Requires the installation of virtualenv:

::

  $ sudo pip install virtualenv

The ACCEL IDSR Input Form uses MongoDB: `See installation instructions <https://docs.mongodb.com/manual/tutorial/install-mongodb-on-debian/>`_


Once you get virtualenv and mongoDB installed and running properly, follow the
steps below:

::

  $ cd ~
  $ git clone https://github.com/naralabs/accel.idsr
  $ cd accel.idsr
  $ virtualenv env


You'll need  to create your own copy of the accel.idsr.ini configuration file,
for which you can copy the file accelidsr/accel.idsr.ini.CHANGEME file, set
your configuration properties there and save as accel.idsr.ini

To run the application ensure you active the virtualenv first:

::

  $ . env/bin/activate

And then, build and start the application

::

  $ pip install -e .
  $ export FLASK_APP=accelidsr
  $ export FLASK_DEBUG=true
  $ flask run
