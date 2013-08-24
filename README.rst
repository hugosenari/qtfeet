===============================
"QTFeet"
===============================

.. image:: https://badge.fury.io/py/qtfeet.png
    :target: http://badge.fury.io/py/qtfeet

.. image:: https://travis-ci.org/hugosenari/qtfeet.png?branch=master
        :target: https://travis-ci.org/hugosenari/qtfeet

.. image:: https://pypip.in/d/qtfeet/badge.png
        :target: https://crate.io/packages/qtfeet?version=latest


"QTFeet, DBus instrospection tool, DFeet clone writed with QT"

* Free software: BSD license
* Documentation: http://qtfeet.rtfd.org.

Features
--------

**DONE**

* Nothing

**TODO**

* Plugin System (all this app are plugin)
* Show available buses in dbus connections
* Show available interfaces in bus
* Show available methods in interface
* Show available properties in interface
* Show available signals in interface
* Show communications events (dbus-monitor)
* Convert interfaces to code
* Call methods in interface
* Get properties in interface (shortcut to call GetProperties)

Some Answers
------------

**Why clone D-Feet?**

I like D-Feet, is useful to me. I Have nothing to do in my vacation and do
something completely new is very hard, then I choose clone something to learn
and tests some concepts.

**Why QT?**

Why not? QT is now GPL, cross platform... This is my first QT attempt,
then is something new to learn.

**How looks (or will look) architecture?**

To be honest I'm trying create something like Eclipse Framework that in the
end can used to create aplications for other uses.

* QT (for UI and some libs like DBus)
* iPOPO (python implementation of OSGi or something close to this)
