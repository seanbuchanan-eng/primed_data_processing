Usage
=====

.. _installation:

Installation
------------

``primed_data_processing`` requires Python 3.10+ and can be installed using pip:

.. code-block:: console

    pip install primed-data-processing

.. _quickstart:

Quick Start
-----------

The primed_data_processing package consists of 7 classes separated into 3 modules.
The modules manage Arbin cycler data, Gamry EIS data, and process raw data files 
into the module classes.

The easiest way to begin working with the PRIMED data is through the :ref:`cellbuilder <cellbuilderapi>` 
module. The cellbuilder module contains a :py:class:`~primed_data_processing.cellbuilder.CellBuilder` 
class with methods for processing Arbin and Gamry data from specific tests performed at PRIMED, 
and building the corresponding Arbin and EIS data structures from the raw data. 

..
    Because of events like equipment failures and power outages, the raw data from the battery tests at PRIMED are rarely uniform.
    Consequently, making a program that would generalize to all tests would be both difficult and require regular maintenance.
    As a result, the primed_data_processing package is inteded to provide a framework for storing and Working
    with the data but relies on the user to perform most of the data processing. That being said, 
    :py:class:`~primed_data_processing.cellbuilder.CellBuilder` contains methods for processing
    data from previous tests that have already been tested. The Quick Start section will cover how to use
    these tools.

To get to know the classes in this package we will start with a simple example with data that can be 
found on the `GitHub repo <https://github.com/seanbuchanan-eng/primed_data_processing>`_. We will start
with the Arbin cycler data and then work towards incorporating EIS data.

To start, import the required modules and classes from ``primed_data_processing``.

.. code-block:: python

    # import modules and classes
    from primed_data_processing.cellbuilder import CellBuilder
    from primed_data_processing.arbin_cycler import ArbinCell, ArbinCycle, ArbinStep

Now build a data manager using the provided classes in ``primed_data_processing``. The .csv file that 
we will be working with is from a test done with Mollicel P42A batteries at PRIMED, for more info see 
:ref:`test info <testb6>`. The data file can be found on the 
`GitHub repo <https://github.com/seanbuchanan-eng/primed_data_processing>`_ under 
test/cycler_testing_data. This test contained multiple steps, cycles, and cells. However,
we have selected a single file from a single cell. Because it is a file from a previous test
at PRIMED we can use the ``CellBuilder`` class to process the data for us. An example using the 
test data is shown below.

.. code-block:: python

    cell_builder = CellBuilder()
    # instantiate a ArbinCell object
    cell = ArbinCell(cell_number=1, channel_number=1)
    local_datapath = 'path/to/B6T10V0_1_2_3_4_9_10_11_12_13_14_15_16_Channel_1.1.csv'

    # select the steps that we want to load. 
    # See PRIMED Test Info in the documentation for step explanations
    steps = {
        'characterization': [6,7,10],
        'degradation': [29]
    }

    # use a method in cell_builder to process the data for us and store in cell.
    cell_builder.read_B6_csv_data(cell=cell, file_path=local_datapath, steps=steps)

Now that we've processed and loaded the data, ``cell`` will contain all of the cycles from the 
data file and each cycle will contain all of the steps with their corresponding data that
occurred in that step. We can then view and manipulate the data using the methods provided in
the :ref:`API documentation <arbinapi>`.

.. code-block:: python


    



Processing Data Using CellBuilder
---------------------------------

Typical raw Arbin test data from PRIMED is .csv or .xlsx files with various column headers such as "Voltage(V)", "Current(A)",
and "Charge_Capacity(Ah)", etc. 