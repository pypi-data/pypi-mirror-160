========================
experimental.catalogplan
========================

.. image:: https://badge.fury.io/py/experimental.catalogplan.svg
    :target: https://badge.fury.io/py/experimental.catalogplan
    :alt: latest release version badge by Badge Fury

.. image:: https://coveralls.io/repos/github/mamico/experimental.catalogplan/badge.svg
    :target: https://coveralls.io/github/mamico/experimental.catalogplan
    :alt: Coveralls status

Introduction
============

* fix plan for unused index in a query https://github.com/zopefoundation/Products.ZCatalog/pull/138

* avoid to have DateRecurringIndex between the valueindexes

Usage
=====

Plone::

    [instance]
    recipe = plone.recipe.zope2instance
    eggs =
        experimental.catalogplan

Zope::

    [instance]
    recipe = plone.recipe.zope2instance
    eggs =
        experimental.catalogplan
    zcml =
        experimental.catalogplan


Warning
=======

This is an experimental addon, mostly safe, but still experimental

**USE AT YOUR OWN RISK**
