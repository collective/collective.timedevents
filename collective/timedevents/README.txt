collective.timedevents Package Readme
=====================================

Overview
--------

collective.timedevents fires clock based Zope 3 events. They can make Zope application react to timers.
This is useful for creating services where something must happen regurlarly or after a certain period has expired.

This is a developer level product. This product is indended to replace Products.TickingMachine with more robust Zope 3 codebase.

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
	    
  Add clock server to tick timedevents subscribers - use your Plone instance name::

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
	    
2. Add collective.timedevents.interfaces.ITickEvent subscribers to your product ZCML declarations.

   Example::

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
	        """ Do something after one hour has elapsed """
	        interval_in_days = 1.0 / 24.0 # One hour, floating point
	        context = site.my_magic_context # Persistent object which stores our timing data
	        if event.last_tick > context.last_action + interval_in_days: # Check whether enough time has elaped
	            do_stuff()
	            context.last_action = event.last_tick # Store when we last time did something
	         
4. You can also to change logging level for logger who log all ticks::
   Just add environment variable TICK_LOGGER_LEVEL to instance part in your buildout.cfg
   
   Example::

       [instance]

       environment-vars += TICK_LOGGER_LEVEL DEBUG


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

Future
------

Cron like "on day/hour/minute X" like subscribers could be added. 

Author
------

Mikko Ohtamaa <mikko.ohtamaa@twinapex.com>

The orignal concept and code was created by Tomasz Cobata Tomasz J. Kotarba <tomasz@kotarba.net>.

`Twinapex Research, Oulu, Finland <http://www.twinapex.com>`_ - High quality Python hackers for hire
