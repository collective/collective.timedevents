collective.timedevents
======================

Overview
--------

collective.timedevents fires clock based Zope 3 events. They can make
Zope application react to timers. This is useful for creating services
where something must happen regurlarly or after a certain period has
expired.

This is a developer level product. This product is indended to replace
Products.TickingMachine with more robust Zope 3 codebase.

There are two different styles of using it:

a) Using the ITickEvent and calculating if action needs to be done in
   the event subscriber. This will also take care of timing over zope
   restarts by keeping event timing persistent.

b) Subscribing to any of the cron-style IIntervalTicks\*-events, not
   worrying about the timing client side. For the longer ticks (weekly,
   montly) a cron-job as trigger makes most sense, in case of zope
   restarts.

Tested by Travis:

.. image:: https://secure.travis-ci.org/collective/collective.timedevents.png?branch=master
   :target: https://travis-ci.org/#!/collective/collective.timedevents

Installation
------------

1. Add collective.timedevents to your buildout by adding the egg to your
   buildout.cfg::

         eggs =
            ...
            collective.timedevents

2. Trigger

Can either be cron-jobs or zope clock-server.

Add clock server to tick timedevents subscribers - use your Plone
instance name::

          [instance]
          ...
              zope-conf-additional =
              <clock-server>
                  method /mysite/@@tick
                  period 90
                  user clockserver-user
                  password password
                  host localhost
              </clock-server>

Or for the cron-like interval-based events, here 900 seconds for the
15-minute event::

          <clock-server>
            method /mysite/@@tick_fifteen
            period 900
            user clockserver-user
            password password
            host localhost
          </clock-server>

Now you should start to see ticks in the zope event log.

Usage
-----

Subscribe to the events/ticks you need.

A. Using the ITickEvent method:

  1. Add collective.timedevents.interfaces.ITickEvent subscribers to your
     product ZCML declarations::

       <configure
       xmlns="http://namespaces.zope.org/zope"
       xmlns:browser="http://namespaces.zope.org/browser"
       i18n_domain="harvinaiset.app">

            <subscriber
                  handler="myproduct.tickers.on_tick"
                  for="collective.timedevents.intefaces.ITickEvent"
                />

       </configure>

  2. Configure your event handler to react after certain period has
     expired::

       from zope.app.component.hooks import getSite

       def on_tick(event):
           """ Do something after one hour has elapsed """
           interval_in_days = 1.0 / 24.0 # One hour, floating point
           context = site.my_magic_context # Persistent object which stores our timing data
           if event.last_tick > context.last_action + interval_in_days: # Check whether enough time has elaped
               do_stuff()
               context.last_action = event.last_tick # Store when we last time did something

B. Using the IIntervalTicks\*-events:

  Add collective.timedevents.interfaces.IIntervalTicks\* subscribers to
  your module ZCML declarations::

       <configure
       xmlns="http://namespaces.zope.org/zope"
       xmlns:browser="http://namespaces.zope.org/browser"
       i18n_domain="mymodule">

            <subscriber
                  handler="myproduct.tickers.on_tick_fifteen"
                  for="collective.timedevents.intefaces.IIntervalTicks15Event"
                />

       </configure>

Other
-----

All ticking code is executed under admin privileges.

ITickEvent tick period is 300 seconds by default. This can be controlled
in views.py.

Ticks for ITickEvent are logged by events.tick\_logger defined in
configure.zcml.

Quality assurance
-----------------

This product fills the following quality criteria:

-  Unit tests provided

-  Good documentation provided

-  Commented code

-  PyPi eggs provided

Author
------

-  ``Mikko Ohtamaa <http://opensourcehacker.com>``\ \_

-  Quintagroup

-  Sune Brøndum Wøller

-  The orignal concept and code was created by Tomasz Cobata Tomasz J.
   Kotarba tomasz@kotarba.net.

-  ``Twinapex Research, Oulu, Finland <http://www.twinapex.com>``\ \_ -
   High quality Python hackers for hire


