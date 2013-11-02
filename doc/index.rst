.. Roäc documentation master file, created by
   sphinx-quickstart2 on Wed Oct 30 22:39:24 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Roäc's documentation!
================================

Contents:

.. toctree::
   :maxdepth: 2

   api

Roäc is an application framework for building system monitoring agents.

It works by executing system-executable plugins in a directory that output
JSON data, and provides triggers to read, modify and add to this information.

A simple application using Roäc looks like::

    #!/usr/bin/env python

    from pprint import pprint
    from roac import Roac

    app = Roac(script_dir='scripts')

    @app.script_handler_by_any
    def print_result(result):
        print '----------------'
        print 'Script: {}'.format(result.name)
        pprint(result.data)
        print '----------------'

    if __name__ == '__main__':
        app.run()


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

