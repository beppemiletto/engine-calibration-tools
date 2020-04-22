.. include:: <isonum.txt>
.. include:: ../_static/figures.txt
.. include:: ../_static/gen/figures.txt

|logo|

HDS SYSTEM OVERVIEW
===================

HDS model-based structure
-------------------------

In below FIGURE is shown a general architecture of HDS system

|gen_010|

In an absolutely general approach to system control, it is basic to define:

*	**External request**: specific demands coming from external environment and aiming to be realized by the system;

*	**Actuators**: physical system which through specific commands, make actions effective;

*	**Sensors**: means by which the control system can monitor the effects of its own commands, verifying if they are realized or not;

**External requests** drive directly the commands: their actuation, through specific control strategies, can be based on two different concepts.

    *	Direct correlation REQUEST-ACTUATION: the control system directly determines the commands to the actuators in function of the specific external requests, through simple maps to be experimentally calibrated and generally different for each application. For each operating point of the system a specific independent map of actuations must be calibrated.

    *	Use of an INTERNAL MODEL: the control system determines the commands to the actuators through internal models aiming to be general and valid for each application and needing a faster calibration. The base of this model is the definition of some internal states, representing the system, and the external requests are converted into specific requests of target value for these internal states.

The choice between an approach based on direct experimental maps and a model-based control system depends generally on the available numbers of actuators and external requests: 

*	For a system with only one degree of freedom (for example only one commanded actuator) and only one external request (for example only torque demand), it is easier and quicker to follow an experimental direct approach, in order to identify the basic correlation between the actuator and the target. Aftermarket systems for passenger cars belong to this category.

*	For systems with several degrees of freedom (many actuators) and several possible requests (for example torque demand, best consumptions, lowest emissions), a model-based approach can reduce a lot the number of calibration tests needed in order to achieve in the best way each target considered as an input. The increasing complexity of actual physical systems, with many available actuators and many possible external requests, suggest to move from a direct experimental-based approach towards an integrated model & calibrations-based approach able to foresee the impact of each actuator each internal state.

|gen_020|

The general characteristics of the **model-based** approach are in FIGURE below.

|gen_030|

The basic external request for an engine is the realization of a requested torque, coming from the driver or from auxiliary vehicle control systems (for example ASR, cruise control, etc.). This torque represents the fundamental internal state of the system. The calculation of the effective torque is based on the calculation of the intermediate efficiencies, collecting the contributes of the different actuator: this is the direct torque determination line (see figure below).

|gen_040|

The direct torque conversion for internal combustion engine must be established as basic relationship for the control system.
 
The other secondary external requests, also important for the engine, are defined through many target values for internal states (FIGURE below). Each internal state represents a measurable value that should be reached in specific engine conditions through particular commands on the actuator. For example, the exhaust manifold must be the highest possible during catalyst light-off phase, and this result can be reached delaying spark advance as much as possible. So, it’s important to establish the effect of each actuator on each internal state interesting for the engine.

|gen_050|

General purpose of control system is to satisfy external requests making direct actions on the system and verifying the effects of these actions through sensors and observers. These feedbacks should be used to monitor single actuator actions (local closed loop controls) and global external requests realization (global closed loop controls) (FIGURE below).

|gen_060|


General overview of HDS Software architecture
---------------------------------------------



The Performance - Torque - Air - throttle opening
+++++++++++++++++++++++++++++++++++++++++++++++++

As all torque-based systems, the action on the accelerator pedal coincides with a torque demand to the ECU, this demand is converted to an air request (through several models present in the software) that is realized through the throttle body opening. A general overview of HDS SW architecture is shown in FIGURE below

|gen_070|

The figure above shows the **TORQUE CONTROL** flow.

.. note::
    The **Bowden cable** from WIKIPEDIA: A Bowden cable is a type of flexible cable used to transmit mechanical force or energy by the movement of an inner cable relative to a hollow outer cable housing. The housing is generally of composite construction, consisting of an inner lining, a longitudinally incompressible layer such as a helical winding or a sheaf of steel wire, and a protective outer covering.

    Before the usage of electronic controlled throttles, the **torque** in Spark Ignited Engine has been controlled using a direct mechanical  connection between the *ACCELERATOR PEDAL* and the *THROTTLE BODY* (included in carburettor before the electronic injection. The mechanical connection was realized by means of the Bowden cable. To change the request for torque from the engine, the driver pressed the accelerator pedal which, being mechanically connected to the throttle, caused a direct variation in its opening.

When the Electronic Throttle Body have been introduced, the *drive by wire* concept has been exploited. HDS system implement a **full developed torque control**. The throttle opening is the final action of a quite long calculation that involve 4 different physical models:

1. The *Performance Demand* - in the figure above is the first upper line of the block diagram. From accelerator pedal, that is a position sensor without mechanical connection to throttle body, comes the driver request (usually for vehicle's motion speed control). This request is combined with additive, subtractive or replacing strategy operators coming from ECU internal controls (e.g. idle control is a replacing terms). **The request is a percentage 0 to 100%**

.. sidebar:: Italian Language Tip
    :subtitle: The Torque and Coppia equivalence

    The HDS SW symbols system uses the acronyms CMU, CME and CMR coming form Italian language Coppia Media Utile, Coppia Media Efettiva a Coppia Media Resistente translated in english respectively into Useful Medium Torque, Medium Effective Torque to Medium Resistant Torque.

2.  The *Torque Demand* -  in the figure above is the second line of the block diagram (flowing from right to left direction). The **torque model of the engine** produces the maximum torque value that the engine can develop and the internal friction to be won for having user's torque available at the engine shaft output. **The torque is measured in N\*m**.

3.  The *Torque to Air Flow* model - Is the leftmost table in block diagram at second to third rows. Since the performance of one Otto cycle is function of the throttled air flow, a model that convert the amount of requested torque into an amount of air to be intaked by engine outputs the **requested air mass quantity expressed in kg/h**.

4.  The *Throttle model* - finally, in the bottom part of the figure, converts the Air Mass Flow to Volume Air Flow before to become a target throttle opening. The **Throttle Opening is expressed in %** where the fully closed throttle is 0% and maximum opening (close to 90 deg. of the blade) is 100%.

The Mixture formation control
+++++++++++++++++++++++++++++

Otto cycle engines work by burning a mixture of comburent and fuel (in our case Air and Natural Gas) mixed in a chemical ratio referred to the stoichiometric one. The amount of air to be provided by means of the throttle actuator is calculated in section `The Performance - Torque - Air - throttle opening`_.

The calculation of the amount of fuel is described in the block diagram in FIGURE below.

|gen_080|

The figure shows in a really synthetic way the macro blocks that put together the most important elements that contribute to the calculation of the so called "**Injection Time**".

.. sidebar:: The Engine Control Slang
    :subtitle: **The TJ aka Injection Time**

    The HDS is an Engine Control System that implement a MultiPoint Sequential Injection (**MPI**). The actuators that are metering the right fuel quantity into the air flow are Injectors. The control of the quantity is made by means of controlling the opening time of the actuator synchronized with the instant when the inlet valve is open. Is commonly used the acronym TJ standing for the Injectors Opening Pulse Duration, in other words the duration of the electric command that drive the opening of the actuators. Commonly expressed in ms, in HDS system is expressed in us.

The delivered fuel amount is calculated mainly by means of 2 controls and 2 model operating synchronized every TDC. A TDC occurs every 720 angle degrees divided by the number of cylinders:

1. *Speed-Density model* - Green field in picture above - The intaked air mass flow is estimated using as input many measured and modeled parameters. Main parameters are the measured Intake Air Manifold Absolute Pressure (aka MAP), the measured Air Temperature, the measured Engine Speed and the modeled (a calibrated look-up table) Intake Efficiency. The Output of the model is a Air MAss flow rate *asAirMain* expressed in **kg/h**

2. *The Target Lambda control* - Light Blue in picture above - Depending from the engine configuration and engine working point a target Air/Fuel ratio (AFR) is calculated. The target is defined as Lambda ratio :math:`\lambda = \frac{AFR_\mathrm{real}}{AFR_\mathrm{stoichiometric}}`. Then the target Lambda is multiplied by the stoichiometric AFR. If the Lambda target is equal to 1.0 it means that the AFR target will be the stoichiometric one that is 17.2 for pure methane Natural Gas. If the Lambda target will be Lean so bigger than 1 (up to 1.5) the AFR target will range between 17.2 * 1 to 17.2 * 1.5. This target output expressed as pure number is used as input for other two different elements.

3. *the AFR closed loop control* - Yellow field in picture - by means of the measured Oxygen concentration in exhaust gas the closed llop control follow the target applying a normalised multiplier to the base fuel quantity. The base fuel quantity is calculated at every TDC dividing the Air Quantity by the target AFR. The Air quantity is previously converted from kg/h to mg/stroke (the white back-grounded blocks calculation). So the fuel quantity at the end is the quantity to be injected by a single actuation of one injector.

4. *The injector model* - Orange field in picture - the single stroke quantity is provided as input to the Injector Model that using some measured parameters and some calibrated table (the physical model of the injector) converts the target quantity to a time expressed in **us** that is then passed to the actuator driver.

The injector is opened for the calculated time and it will deliver into the air flow the correct amount of fuel.

The Ignition Control
++++++++++++++++++++

We dealt in the section "`The Performance - Torque - Air - throttle opening`_" on how to supply the correct amount of air to the engine. In the section "`The Mixture formation control`_" we dealt instead with how the HDS system supplies the right amount of fuel in relation to the air actually sucked by the engine. In this section we will deal with the third fundamental component for Otto cylinder engines: ignition. It is no coincidence that Otto cycle engines are also called spark ignition engines.

The HDS implements an ignition system for active coils, i.e. ignition coils in which the electronic power circuitry is integrated. The active coils are powered externally with respect to the ECU and receive from it only the activation command which from the electronic point of view is a digital ON - OFF signal. By means of the command, the current that charges the primary winding is criculated. When the target current is reached, the circuit on the coil causes the discharge of the same which leads to the generation of high voltage on the secondary winding and therefore to the discharge of the spark. So from the point of view of control, ignition consists of a simple model of charging the current in the coil. See figure below.

|gen_085|

The time for charging the coil is called Dwell Time and is function of the coils supply voltage. The voltage is measured by HDS and used as imput for a 1D look-up table that output the time expressed in **us**. After this point it matter of low level driver that take care of scheduling the command execution on a angle based timing.

.. sidebar:: The Engine Control Slang
    :subtitle: **The "Spark Advance"**

    In motoring jargon the term "spark advance" refers to the angle that the crankshaft makes between the point where the spark is struck and the (normally) subsequent achievement of the top dead center (TDC). It goes without saying that if the first point reached is the TDC and the spark occurs later, the ignition advance value is negative.

The most important component of ignition control is undoubtedly the ignition advance calculation. It is not within the scope of this manual to explain the importance of applying the correct ignition advance for the purpose of controlling both combustion and torque. We limit ourselves to specify that HDS uses as an angular reference for the advance of the ignition top dead center of the cylinder which is located at the end of the compression phase: this point corresponds to zero (0). All the angles which, with respect to the direction of rotation of the motor, precede said point belong to the positive range of the advance values. Vice versa, the following angles are in the field of negative values.

The main contributions of the ignition calculation chain are shown in the figure below.

|gen_090|

The final value of the ignition advance that is applied to each TDC is the result of a calculation in which different operators modify an initial value, called the base value. The calculation chain exclusively provides for additive or subtractive terms. The most important are summarized below:

1. *The tables of the basic advance* - in the green field in the figure - corresponds to the advance value identified during the calibration according to the desired optimizations. For example consumption and emissions. Represents the advance value that is used in normal engine conditions. Different tables are selected according to the engine operating mode. The example shows only the normal and cut - off condition tables (also known as deceleration fuel shut off DFSO or absence of fuel injection during the rapid deceleration phase).

2. *The correction for EGR presence* - in the light blue field in the figure - the correction is calculated on the basis of the percentage of EGR that flows into the intake manifold;

3. *The correction for Lambda* - in the gray field in the figure - if the title of the mixture differs from the stoichiometric value, an advance correction is applied. Normally lean combustion requires higher advances than stoichiometric combustion;

4. *Dynamic correction for fast idle control* - in the yellow field in the figure - The idle speed control strategy uses the spark advance as a quick actuation for torque variations.

5. *Dynamic correction for detonation control* - in the orange field in the figure - The strategy of detonation control uses variations of the ignition advance calculated cylinder by cylinder in order to homogenise the optimized combustion between the cylinders near the maximum Torque Output.


The other main functions
++++++++++++++++++++++++

The three chapters before made a general overview of the main control functions meaning the function that must be used to run an engine.

HDS provides several more "auxiliary" functions. Among them we just remind the most important:

1. *The Boost Pressure Control* - Using a dedicated boost pressure sensor controls in closed loop this parameter for engine provided with controlled turbocharger unit.

2. *The EGR control* - Complex strategy for managing the Exhaust Gas Recirculation used to limit NOx emissions and / exhaust temperature

3. *The Knocking detection and Control* - Uses up to two knocking sensors placed on the engine block. Is divided into Soft Knocking and Hard Knocking detection and is used respectively for performance optimisation and / or engine safety.

4. *The misfire diagnosis* - based on crankshaft wheel acceleration detect method ensure the safe operation of engine even in case of not diagnosable components failures, e,g, the spark plugs.

5. *The full set of diagnosis strategy* - Fully covering both sensors and actuators as well as internal ECU working parameters.

6. *Safety functions* - Running at key on or runtime they cover all the `3-Layer EGAS Safety Concept, <https://www.its-mobility.de/download/FuSi/Dokumentation/Richter_Folien_FuSi_2017.pdf>`_.

7. *The full set of Euro VI / China VI compliancy functions* that include diagnosis, statistics, errors publication, cyber security, ....

The complete list of functions and subfunctions is very long and will be partially treated in following sections.

