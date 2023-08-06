================
pySerialSensors
================

.. image:: https://img.shields.io/pypi/v/pyserialsensors.svg
        :target: https://pypi.python.org/pypi/pyserialsensors

.. image:: https://img.shields.io/travis/Egenskaber/pyserialsensors.svg
        :target: https://travis-ci.com/Egenskaber/pyserialsensors

.. image:: https://readthedocs.org/projects/pyserialsensors/badge/?version=latest
        :target: https://pyserialsensors.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/Egenskaber/pyserialsensors/shield.svg
     :target: https://pyup.io/repos/github/Egenskaber/pyserialsensors/
     :alt: Updates



Serial communication with sensors via I2C, SPI and UART using FTDI USB bridges

Make sure your current user is member of the `dialout` group.


* Free software: MIT license
* Documentation: https://pyserialsensors.readthedocs.io.

Development
-----------

Setup the FTDI USB interface using [PyFTDI installation instructions](https://eblot.github.io/pyftdi/installation.html).

Install git and clone the repository

.. code-block:: bash

    git clone https://gitlab.com/Egenskaber/pyserialsensors.git

Install all requirements via
.. code-block:: bash

    pip install -r MMS/requirements.txt

To test your installation connect a supported I2C or SPI sensor and run

.. code-block:: bash

    python -m pyserialsensors.examples.example_single_read


Supported Sensors
------------------

* SHT85
* SFM3000, 3200, 3300
* SFM4100, 4200, 4300
* SDP810
* SPS30
* BME280
* SCD30
* ADS1015
* MAX31865
* SMGAir2
* S8000 dew point mirror


Rename FTDI
------------

Use tools/rename.py

Check the result using 

.. code-block:: bash

    lsusb -d 0403: -v

Known Issues
------------

- All SFM sensors are indicated as SFM3XXX

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
