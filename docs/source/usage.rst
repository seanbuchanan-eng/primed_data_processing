Usage
=====

This section explains how to use the ``primed_data_processing`` package.

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

To get to know the classes in this package we will start with a simple example with data that can be 
found on the `GitHub repo <https://github.com/seanbuchanan-eng/primed_data_processing>`_. We will start
with the Arbin cycler data and then work towards incorporating EIS data.

All of the following code examples can be found on the GitHub repo in ``examples/``.

Working With Cycler Data
~~~~~~~~~~~~~~~~~~~~~~~~

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

All Arbin cycler objects in this package are iterable; therefore, there is two ways to access the
cycles and steps within ``cell``. To show an example we will use the ``get_data_as_dataframe()``
to get the data as a Pandas DataFrame for step 10.

.. code-block:: python

    # Using loops
    for cycle in cell:
        if cycle.cycle_index == 1:
            for step in cycle:
                if step.step_index == 10:
                    step.get_data_as_dataframe()

    # Using object attributes
    cell.cycles[0].get_step(10)[0].get_data_as_dataframe()

As shown above we can use either loops or the provided method ``get_step(step number)`` in the cycle
object to get a list of the step `step number` that occur in the cycle.

Adding, observing, and manipulating data is mostly confined to the 
:py:class:`~primed_data_processing.arbin_cycler.ArbinStep` object. The ``ArbinStep`` object has the 
methods :py:meth:`~primed_data_processing.arbin_cycler.ArbinStep.get_data_as_dataframe` and 
:py:meth:`~primed_data_processing.arbin_cycler.ArbinStep.get_data_as_array` for observing data. The
data can then be manipulated using the returned data structures. Additionally, ``ArbinStep`` itself acts
like a python dictionary so that the data can be accessed using key-word identifiers. The keys are based 
on what headers are in the original data files. To get a list of the headers there is two options.

.. code-block:: python

    # Using cell (preferred method)
    cell.headers

    # Using the data_dict attribute
    cell.cycles[0].get_step(10)[0].data_dict.keys()

The headers can be used to select specific data from the ``ArbinStep``. 

.. code-block:: python

    # Get step
    step = cell.cycles[0].get_step(10)[0]
    
    # Get voltage data from the step
    voltage = step['Voltage(V)']

The final option provided by ``ArbinStep`` is to quickly plot data using the 
:py:meth:`~primed_data_processing.arbin_cycler.ArbinStep.plot_step_column` method. The plotting
method plots a single feature in the step, such as voltage.

.. code-block:: python
    
    # Get step
    step = cell.cycles[0].get_step(10)[0]

    # Plot voltage
    step.plot_step_column('Voltage(V)')

Working With Gamry EIS Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Working with the Gamry EIS data is a bit different to the Arbin data. Because the EIS .DTA files don't contain 
any information about where they came from in the test, i.e what cycle number or cell number, it's up to the 
user to properly configure the data. To do so, we will use the :ref:`Gamry API documentation <gamryapi>`.

Like the Arbin data, we will use the provided example data on the
`GitHub repo <https://github.com/seanbuchanan-eng/primed_data_processing>`_ 
under test/eis_testing_data. To start, make the necessary imports.

.. code-block:: python

    from primed_data_processing.gamry_eis import EisSweep, EisCycle, EisCell

Now we import the data using the ``EisSweep`` method 
:py:meth:`~primed_data_processing.gamry_eis.EisSweep.read_DTA_file`.

.. code-block:: python

    path = 'path/to/B6T10V0_Chan001_Cycle001_Step014.DTA'

    # Make EisSweep object to store the data
    # from the Arbin data we know that eis steps happen at 50% soc
    eis_sweep = EisSweep(name='eis cycle 1', soc=0.5, step_index=14)

    # import the data
    eis_sweep.read_DTA_file(path)

As you can see, the EIS data filenames contain the channel and cycle that 
they came from. We will use this fact extensively when processing the data.
Now we can put the sweep into cycle and cell objects. This step is obviously
unnecessary for just a single ``EisSweep``, however, it is helpful to illustrate
the process so that when a test has multiple EIS sweeps at different SOC's in
a single cycle they can be organized and easily indexed.

.. code-block:: python

    # Make an EisCycle object
    cycle = EisCycle(cycle_number=1, sweeps=[eis_sweep], name='cycle1')

    # Make an EisCell object
    cell = EisCell(cell_number=1, channel_number=1, name='cell1', eis_cycles=[cycle])

We now see the same structure as the Arbin data start to form with the ``cell[cycle[step]]``
type packaging.

Now we can inspect the data similarly to Arbin data using 
:py:meth:`~primed_data_processing.gamry_eis.EisSweep.get_data_as_array` and 
:py:meth:`~primed_data_processing.gamry_eis.EisSweep.get_data_as_dataframe`. 

.. code-block:: python

    cell.cycles[0].sweeps[0].get_data_as_dataframe()
    cell.cycles[0].sweeps[0].get_data_as_array()

Merging Arbin and Gamry Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you've been following along through the whole `Quick start` section, you
may be thinking that accessing the EIS data with the Arbin data would be nice.
Combining the data would allow for easy access of step temperatures, discharge 
capacities, etc. during the same cycle as the EIS.

To support this functionality for the B6 dataset, the CellBuilder method 
:py:meth:`~primed_data_processing.cellbuilder.CellBuilder.merge_B6_eis_data`
merges the two data sets together. Once merged, the EisSweeps can be accessed
from the corresponding ``ArbinStep`` using 
:py:meth:`~primed_data_processing.arbin_cycler.ArbinStep.get_eis_step`. For more
details see the tutorial notebook on 
`GitHub <https://github.com/seanbuchanan-eng/primed_data_processing>`_ and the 
documentation for ``merge_B6_eis_data()``.

Although ``CellBuilder`` provides helper methods for easy processing of data 
from previous tests at PRIMED, the ultimate intention of this package is to 
provide a framework for using the data. The actual processing of the data is 
largely meant to be left to the user. This is because every new test produces
a new dataset with it's own pitfalls and uniqueness that make it extremely hard 
to generalize the data processing. 

To help with this more complex data processing and importing, examples are shown
in the next section :ref:`Advanced Data Importing <advancedDataImporting>`.

.. _advancedDataImporting:

Advanced Data Importing
-----------------------

This section expands on what was covered in the :ref:`Quick Start <quickstart>` 
section by importing full tests with multiple files. To try this example you will
need access to the full B6T10V0 dataset 
( `contact <https://onlineacademiccommunity.uvic.ca/primed/>`_ )
and have it downloaded locally. Once the data is downloaded import the required packages.

.. code-block:: python

    from primed_data_processing.cellbuilder import CellBuilder
    from primed_data_processing.arbin_cycler import ArbinCell, ArbinCycle, ArbinStep
    from primed_data_processing.gamry_eis import EisSweep, EisCycle, EisCell

    import os

Next, we will import the Arbin data using ``CellBuilder``. Make sure that the file structure
hasn't been changed since you downloaded it. As long as the file structure remains the 
same as when it was downloaded the test can be imported as below.

.. code-block:: python

    # instantiate CellBuilder
    cell_builder = CellBuilder()

    raws_prepath = 'path/to/raws/'

    # all channel and cell numbers from B6 in order
    channel_numbers = (1,2,3,4,9,10,11,12,13,14,15,16)
    cell_numbers = (9,10,11,12,1,2,3,4,5,6,7,8)

    # list for holding processed cells
    arbin_cells = []

    # loop over channel numbers
    for channel_idx, channel in enumerate(channel_numbers):
        print(f'Processing channel {channel}')

        # make subfolder name in raws folder
        folder_name = f'B6T10V0_1_2_3_4_9_10_11_12_13_14_15_16/Channel_{channel}/'

        # append new cell to cells processed cells list
        arbin_cells.append(ArbinCell(cell_numbers[channel_idx], channel))

        # get directory of the current folder
        directory = os.fsencode(raws_prepath+folder_name)

        # loop over all files in the current directory
        for file in os.listdir(directory):
            # get filename
            filename = os.fsdecode(file)

            # ignore .xlsx files
            if filename.endswith('.csv'):
                # process file with CellBuilder method
                cell_builder.read_B6_csv_data(
                    arbin_cells[channel_idx], # current cell being processed
                    raws_prepath+folder_name+filename, # path to file being processed
                    {'characterization': [10,13,14]}, # steps to save
                    verbose=False # minimal printouts
                )

Next, import EIS data in a similar manner.

.. code-block:: python

    # Load eis into objects
    file_prepath = 'path/to/raws/B6T10V0_1_2_3_4_9_10_11_12_13_14_15_16/EIS/'

    # all channel and cell numbers from B6 in order
    channel_numbers = (1,2,3,4,9,10,11,12,13,14,15,16)
    cell_numbers = (9,10,11,12,1,2,3,4,5,6,7,8)

    # list for holding processed cells
    eis_cells = []

    # loop over all channels in the batch
    for channel_idx, channel in enumerate(channel_numbers):
        # initial cycle number
        cycle = 1

        # list for storing processed cycles
        eis_cycles = []

        # loop until cycle number 23.
        while cycle <= 23:

            # make a new EisSweep for every cycle (only 1 sweep per cycle in this case)
            eis_sweep = EisSweep(f'eis cycle{cycle}', 0.5, 14)

            # handle different file and cycle combinations in the .DTA filename.
            if cycle < 10 and channel < 10:
                eis_sweep.read_DTA_file(file_prepath + f'B6T10V0_Chan00{channel}_Cycle00{cycle}_Step014.DTA')
            elif cycle < 10 and channel < 100:
                eis_sweep.read_DTA_file(file_prepath + f'B6T10V0_Chan0{channel}_Cycle00{cycle}_Step014.DTA')
            elif cycle < 100 and channel < 10:
                eis_sweep.read_DTA_file(file_prepath + f'B6T10V0_Chan00{channel}_Cycle0{cycle}_Step014.DTA')
            elif cycle < 100 and channel < 100:
                eis_sweep.read_DTA_file(file_prepath + f'B6T10V0_Chan0{channel}_Cycle0{cycle}_Step014.DTA')
            else:
                print('Cycle number greater than 100!')

            # add a new EisCycle to the cycles list for every cycle
            eis_cycles.append(EisCycle(cycle, [eis_sweep], f'cycle_object_{cycle}'))
            cycle += 2
            
            
        # make the EisCell object with all of the processed data
        eis_cells.append(EisCell(
            name=f'eis step for channel{channel}', 
            eis_cycles=eis_cycles, 
            cell_number=cell_numbers[channel_idx], 
            channel_number=channel)
            )
        # reset the cycles list for the new cell.
        eis_cycles = []

Then we can merge the two datasets together,

.. code-block:: python

    cell_builder.merge_B6_eis_data(eis_cells, arbin_cells)

and inspect and consume the data using the ``ArbinCell`` methods described in the 
:ref:`Quick Start <quickstart>` section.

For more examples see 
`examples <https://github.com/seanbuchanan-eng/primed_data_processing/tree/main/examples>`_
on GitHub.