PRIMED Test Info
================

This page desicribes the making and format of past battery tests at PRIMED.

General Format
--------------

Major tests at primed all follow the same general naming convention. An example of a 
test name from a previous test is **B6T10V0**.

The test name starts with a **B** representing the batch of cells that is tested together. In
this case, batch 6 is a batch of Mollicel P42A cells. This is followed by the test number **T10**.
The test number represents the order of steps within the test. The final character **V**,
indicates the version number of the test. The version number is changed if the same 
test is run with different parameters like C-rates or DOD's. The provided data files will 
start with the test name followed by underscores and numbers representing the channel 
numbers in the test and a final **_channel_#** that indicates what channel the file refers to.
An example file name is shown below.

.. code-block:: text

    B6T10V0_1_2_3_4_9_10_11_12_13_14_15_16_Channel_1

Test summaries will eventually be added to the documentation; unfortunately, they are 
currently only available upon request via contact through the 
`PRIMED website <https://onlineacademiccommunity.uvic.ca/primed/>`_.

Smaller, informal, experiments that last no longer than a week are givin miscellaneous names
that indicate what the experiment was used for. An example would be **leaf_characterization**
for an experiment that characterizes Nissan Leaf batteries.

.. _testb6:

B6: Mollicel P42A Test
----------------------------

The B6 dataset is the largest dataset currently at PRIMED. It consists of 16 Mollicel P42A cells 
that were cycled under varying conditions. The test consists of a characterization cycle and a 
degradation cycle. The degradation cycle runs continuously except for when it is interrupted by 
the characterization cycle every 14 days. There are 3 test versions that are run in batch 6, however,
they all share the same characterization cycle.

Characterization Cycle
~~~~~~~~~~~~~~~~~~~~~~

The characterization cycle for B6 tests has the following steps:

1. Set chamber temperature to :math:`T_a = 23^{\circ}` C
2. 4 hour rest (temperature soak)
3. CC discharge at C-rate = -1/3 until minimum voltage
4. 1 hour rest
5. CC charge at C-rate = 1/3 until maximum voltage
6. CV charge at maximum voltage to cutoff current :math:`I = \frac{Nominal Capacity}{100}`
7. 1 hour rest
8. CC discharge at C-rate = -1/3 until minimum voltage
9. 1 hour rest
10. CC charge at C-rate = 1/3 until :math:`\int_{t_0}^{t} i(t)\,dt\ = (Step \text{ } 8 \text{ } Discharge Capacity)/2`
11. 1 hour rest
12. EIS test from 100kHz-1Hz
13. 10 min rest
14. Direct current internal resistance test
15. 10 minute rest
16. CC charge at C-rate = 1/3 until :math:`\int_{t_0}^{t} i(t)\,dt\ = (Step \text{ } 8 \text{ } Discharge Capacity)*DOD_i/2`

Test 10 Degradation Cycle
~~~~~~~~~~~~~~~~~~~~~~~~~

The degradation cycle for T10 has the following steps:

1. Set chamber temperature to :math:`T_a = 35^{\circ}` C
2. 4 hour rest (temperature soak)
3. CC charge at 1C to maximum voltage
4. CV charge at maximum voltage to cutoff current :math:`I = \frac{Nominal Capacity}{20}`
5. 20 minute rest
6. CC discharge at :math:`C_i` until :math:`\int_{t_0}^{t} i(t)\,dt\ = (Nominal Capacity)*DOD_i`
7. 20 minute rest
8. Return to step 3

where :math:`C_i` and :math:`DOD_i` will be different C-rates and depths-of-discharge for different 
channels.

Test 11 Degradation Cycle
~~~~~~~~~~~~~~~~~~~~~~~~~

Coming Soon.

Test 12 Degradation Cycle
~~~~~~~~~~~~~~~~~~~~~~~~~

Coming Soon.

B6 Test Index
~~~~~~~~~~~~~

.. csv-table::
    :header: "Step", "Test 10", "Test 11", "Test 12"
    :widths: 20, 35, 35, 35
    :align: left
    
    1	,Start	    ,Start	    ,Start
    2	,C Reset	,C Reset	,C Reset
    3	,C CC Dis	,C CC Dis	,C CC Dis
    4	,C Rest	    ,C Rest	    ,C Rest
    5	,C Reset	,C Reset	,C Reset
    6	,C CC Cha	,C CC Cha	,C CC Cha
    7	,C CV Cha	,C CV Cha	,C CV Cha
    8	,C Rest	    ,C Rest	    ,C Rest
    9	,C Reset	,C Reset	,C Reset
    10	,C CC Dis	,C CC Dis	,C CC Dis
    11	,C Rest	    ,C Rest	    ,C Rest
    12	,C CC Cha	,C CC Cha	,C CC Cha
    13	,C Rest	    ,C Rest	    ,C Rest
    14	,ACIM	    ,ACIM	    ,ACIM
    15	,C Rest	    ,C Rest	    ,C Rest
    16	,IR	        ,IR	        ,IR
    17	,C Rest	    ,C Rest	    ,C Rest
    18	,C Reset	,C Rest	    ,C Rest
    19	,C CC Cha	,D Reset	,D Reset
    20	,C Rest	    ,D CC Dis	,D Rest
    21	,C Reset	,D Rest	
    22	,C Rest	    ,D CC Cha	
    23	,D CC Dis	,D Rest	
    24	,D Reset	,D Reset	
    25	,D Rest	    ,Sim	
    26	,D CC Cha		
    27	,D CV Cha		
    28	,D Rest		
    29	,D CC Dis		
    30	,D Reset		
    31	,D Rest		

