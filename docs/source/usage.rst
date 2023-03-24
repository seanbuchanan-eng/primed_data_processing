Usage
=====

.. _installation:

Installation
------------

To use primed_data_processing, first install it using pip:

.. code-block:: console

    pip install primed-data-processing

.. _quickstart:

Quick Start
-----------

The primed_data_processing package consists of 7 classes seperated into 3 modules.
The modules correspond to their purpose of managing Arbin cycler data, managing
Gamry EIS data, or processing the raw data files into the designed data structures.

The typical entry point into the package is through the :ref:`cellbuilder <cellbuilderapi>` module. 
The cellbuilder module contains a :py:class:`~primed_data_processing.cellbuilder.CellBuilder` class with with methods
for processing Arbin and Gamry data from specific tests at PRIMED, and building the corresponding data structures. Because
of events like equipment failures and power outages, the raw data from the battery tests at PRIMED are rarely uniform.
Consequently, making a program that would generalize to all tests would be both difficult and require regular maintenance.
As a result, the primed_data_processing package is inteded to provide a framework for storing and Working
with the data but relies on the user to perform most of the data processing. That being said, 
:py:class:`~primed_data_processing.cellbuilder.CellBuilder` contains methods for processing
data from previous tests that have already been tested. The Quick Start section will cover how to use
these tools.

First, we will work with the Arbin cycler data. There is multiple datasets from the Arbin cycler; however,
we will work with a single example file to start.

First, import the required modules and classes.

.. code-block:: python

    # import modules and classes
    from primed_data_processing.cellbuilder import CellBuilder
    from primed_data_processing.arbin_cycler import ArbinCell, ArbinCycle, ArbinStep

Now we build a data manger using the provided classes. The .csv file that we will be working
with is from a test done with Mollicel P42A batteries at PRIMED. It is on the GitHub repo under
test/cycler_testing_data. This test contained multiple steps, cycles, and cells. However,
we have selected a single file from a single cell. Because it is a file from a previous test
at PRIMED we can use the ``CellBuilder`` class to process the data for us. An example using the 
test data is shown below.

.. code-block:: python

    cell_builder = CellBuilder()
    # instantiate a ArbinCell object
    cell = ArbinCell(cell_number=1, channel_number=1)
    local_datapath = 'path/to/B6T10V0_1_2_3_4_9_10_11_12_13_14_15_16_Channel_1.1.csv'

    # select the steps that we want to load
    steps = {
        'characterization': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        'degradation': [...]
    }
    # use a method in cell_builder to process the data for us.
    cell_builder.read_B6_csv_data(cell=cell, file_path=local_datapath, steps=steps)

Now that we've processed and loaded the data, ``cell`` will contain a list of cycles from the 
data file and each cycle will contain a list of steps with their corresponding data that
occured in that step. We can view and manipulate the data using the methods provided in
``ArbinStep``.
    



Processing Data Using CellBuilder
---------------------------------

Typical raw Arbin test data from PRIMED is .csv or .xlsx files with various column headers such as "Voltage(V)", "Current(A)",
and "Charge_Capacity(Ah)", etc. 