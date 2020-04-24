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

The fundamental instrumentation for calibrate HDS
-------------------------------------------------

We all know that the development of an engine application may require a huge amount of engineering efforts and this manual is not intended for explain how to do it. The instrumentation used may vary a lot depending on a lot of availabilities, requirements, personal approaches, environmental contexts, time to market, technological constraints, ....

**HDS application development strongly requires** few instrumentation to exploit properly the provided Engine Control System features. Following chapters will go through these items with an *how?, where?, when? and why?* approach, stating that the answer to *who?* question is simply *you*, the reader.

The Mass Air Flow measure
+++++++++++++++++++++++++

* *HOW?* An Air Flow sensor that can measure the Mass of Air intaked by the engine capable of provide the measure mainly in steady state. The accuracy of the measure is more relevant than the response time. The range may be the real problem since the amount of air may very of one order of magnitude. The best solution is to integrate and use a Hot Film MAF directly connected to the HDS. This solution also provides two helpful features:

    a. the measure will be available in the same context of the development tools (e.g. Canape or Inca)

    b. is possible to set (for development) the measured air instead of the estimated air for controlling the injection.

.. sidebar:: Hot-Film Air-Mass Meters
    :subtitle: A standard Automotive Mass Production Components

    |sys_020|

* *WHERE?* The measure must be done in order to include the air intaked by the engine. The most suitable position of the sensor is the air intake pipe after the filter before the compressor in case of Turbocharged engine or the intake manifold in case of normally aspirated engine.

* *WHEN?* The measure must be available during the calibration of the torque request, air demand and air measure functions. That represent the 80% of the base calibration.

* *WHY?* The torque management in Otto cycle engines is driven by means of air throttling. The HDS provides a complete set of functions for managing the intaked air for:

    * Requested Torque generation

    * Management of the injection

    * Ensure the safety of the Powertrain

    * Provide the diagnosis output in case of malfunctioning of components non covered by direct diagnosis

The Cylinder Pressure measure
+++++++++++++++++++++++++++++

* *HOW?* Also called **indicating system** the sAn Air Flow sensor that can measure the Mass of Air intaked by the engine capable of provide the measure mainly in steady state. The accuracy of the measure is more relevant than the response time. The range may be the real problem since the amount of air may very of one order of magnitude. The best solution is to integrate and use a Hot Film MAF directly connected to the HDS. This solution also provides two helpful features:

    a. the measure will be available in the same context of the development tools (e.g. Canape or Inca)

    b. is possible to set (for development) the measured air instead of the estimated air for controlling the injection.

.. sidebar:: Hot-Film Air-Mass Meters
    :subtitle: A standard Automotive Mass Production Components

    |sys_020|

* *WHERE?* The measure must be done in order to include the air intaked by the engine. The most suitable position of the sensor is the air intake pipe after the filter before the compressor in case of Turbocharged engine or the intake manifold in case of normally aspirated engine.

* *WHEN?* The measure must be available during the calibration of the torque request, air demand and air measure functions. That represent the 80% of the base calibration.

* *WHY?* The torque management in Otto cycle engines is driven by means of air throttling. The HDS provides a complete set of functions for managing the intaked air for:

    * Requested Torque generation

    * Management of the injection

    * Ensure the safety of the Powertrain

    * Provide the diagnosis output in case of malfunctioning of components non covered by direct diagnosis



