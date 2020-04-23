.. include:: <isonum.txt>
.. include:: ../_static/figures.txt
.. include:: ../_static/sys/figures.txt

|logo|

Engine Instrumentation & Development Tools
==========================================

Recommended Engine Instrumentation
----------------------------------

Before starting the calibration of a new engine on the test bench, it’s necessary to have a complete control of all engine system, from air intake to exhaust gas. In particular it’s mandatory to control the temperatures of the head engine and of turbine inlet and outlet in order to maintain them, during the calibration, lower than limits fixed for materials.
As engine instrumentation has to be customized for each application it’s not possible to give detailed instructions always valid.
For the calibration work a typical engine instrumentation is reported in FIGURE below:

|sys_010|

The functions and priority of single instrumentation are in table below

+--------------------------+--------------------------------------------+------------------------------+
| Instrumentations         |    Functions                               |  Priority                    |
+==========================+============================================+==============================+
|  Mass air flow meter     |    to calibrate the speed density model    |  Mandatory                   |
+--------------------------+--------------------------------------------+------------------------------+
|  Cyl. Press. Sensors     |    monitoring combustion                   |  Mandatory at least one cyl. |
+--------------------------+--------------------------------------------+------------------------------+
|  UEGO sensor             |    to verify Air Fuel Ratio                |  Mandatory                   |
+--------------------------+--------------------------------------------+------------------------------+
|  T inlet turbocharger    |   to estimate turbocharger work,           |  Mandatory                   |
+--------------------------+   material stress and                      +------------------------------+
|  T outlet turbocharger   |   to improve efficiency during calibration |  Optional                    |
+--------------------------+--------------------------------------------+------------------------------+
|  T exhaust single ducts  |   monitor combustion balance among cyls.   |  Optional                    |
+--------------------------+--------------------------------------------+------------------------------+
|  T in / out catalyst     |    to verify catalyst efficiency           |  Optional                    |
+--------------------------+--------------------------------------------+------------------------------+
|  Environment conditions  |    to set the base parameters              |  Optional                    |
+--------------------------+--------------------------------------------+------------------------------+

