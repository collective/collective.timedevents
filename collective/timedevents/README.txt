collective.timedevents Package Readme
=====================================

Overview
--------

collective.timedevents fires clock based Zope 3 events. They can make Zope application react to the computer clock.
This is useful for creating services where something must happen regurlarly or after a certain period of time has expired.

This is a developer level product.

Usage
-----

1. Install collective.timedevents

  Add the following to your buildout.cfg::
  
    eggs = 
	    ...
	    collective.timedevents
	    
    zcml = 
        ...
	    collective.timedevents
	    
  Add clock server to tick timedevents subscribers::
	  [instance]
	  ...
		  zope-conf-additional =
		  <clock-server>
		      method /mysite/@@tick
		      period 90
	    	  user admin
		      password adminpassword
		      host localhost
		  </clock-server>
	    
2. Add collective.timedevents.interfaces.ITickEvent subscribers to your product ZCML declarations::

   <configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    i18n_domain="harvinaiset.app">

		<subscriber
		      handler="myproduct.tickers.on_tick"
		      for="collective.timedevents.intefaces.ITickEvent"
		    />

    </configure>
    
3. Configure your event handler to react after certain period has expired::

    from zope.app.component.hooks import getSite

    def on_tick(event):
    
        interval_in_days = 1.0 / 24.0 # One hour, floating point
        context = site.my_magic_context
        if event.last_tick > context.last_action + interval_in_days:
            do_stuff()
            context.last_action = event.last_tick
         


Other
-----

All ticking code is executed under admin privileges.
Tick period is 300 seconds by default. This can be controlled in views.py. 
Ticks are logged by events.tick_logger defined in configure.zcml.

The product is loosely connected to Plone, but can be used standalone with little modifications.

Quality assurance
-----------------

This product fills the following quality criteria:

* Unit tests provided

* Good documentation provided

* Commented code

* PyPi eggs provided

Author
------

Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>

The orignal concept and code was created by Tomasz Cobata Tomasz J. Kotarba <tomasz@kotarba.net>.

`Twinapex Research, Oulu, Finland <http://www.twinapex.com>`_ - High quality Python hackers for hire
