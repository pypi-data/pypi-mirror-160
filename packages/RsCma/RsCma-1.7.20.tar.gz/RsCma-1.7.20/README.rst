==================================
 RsCma
==================================

.. image:: https://img.shields.io/pypi/v/RsCma.svg
   :target: https://pypi.org/project/ RsCma/

.. image:: https://readthedocs.org/projects/sphinx/badge/?version=master
   :target: https://RsCma.readthedocs.io/

.. image:: https://img.shields.io/pypi/l/RsCma.svg
   :target: https://pypi.python.org/pypi/RsCma/

.. image:: https://img.shields.io/pypi/pyversions/pybadges.svg
   :target: https://img.shields.io/pypi/pyversions/pybadges.svg

.. image:: https://img.shields.io/pypi/dm/RsCma.svg
   :target: https://pypi.python.org/pypi/RsCma/

Rohde & Schwarz CMA180 Radio Tester Driver RsCma instrument driver.

Basic Hello-World code:

.. code-block:: python

    from RsCma import *

    instr = RsCma('TCPIP::192.168.56.101::5025::SOCKET', reset=True)
    idn = instr.query('*IDN?')
    print('Hello, I am: ' + idn)

Check out the full documentation on `ReadTheDocs <https://RsCma.readthedocs.io/>`_.

Supported instruments: CMA180

The package is hosted here: https://pypi.org/project/RsCma/

Documentation: https://RsCma.readthedocs.io/

Examples: https://github.com/Rohde-Schwarz/Examples/tree/main/RadioTestSets/Python/RsCma_ScpiPackage


Version history:
----------------

    Latest release notes summary: Update for Firmware 1.7.20

    Version 1.7.20.28
        - Update for Firmware 1.7.20

    Version 1.7.10.26
        - Fixed bug in interfaces with the name 'base'

    Version 1.7.10.24
        - Update for Firmware 1.7.10
        - Fixed several misspelled errors

    Version 1.5.70.22
        - Added documentation on ReadTheDocs

    Version 1.5.70.21
        - Added new data types for commands accepting numbers or ON/OFF:
        - int or bool
        - float or bool

    Version 1.5.70.0018
        - First released version
