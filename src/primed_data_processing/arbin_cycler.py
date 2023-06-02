# Sean Buchanan
# This module is intended to be an easy to use datastructure for
# Arbin battery data produced at PRIMED.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .gamry_eis import EisSweep

class ArbinStep:
    """
    Represents a step in an Arbin MITS PRO test schedule.

    An example of a step would be a constant current discharge from some beginning
    SOC to some ending SOC or voltage.

    Attributes
    ----------
    ``name`` \: ``str``
        Name of the step.
    ``step_index`` \: ``int``
        The step number.
    ``step_type`` \: ``str``
        The type of the step can be any of 'initialization', 'characterization', 'degradation'.
    ``data_dict`` \: ``dict[str: any]``
        Dictionary of data that mimics the input file format. Keys are the column headers from
        an Arbin data csv and the values are the column data associated with the headers.

    Methods
    -------
    """
    
    def __init__(self, step_index: int, step_type: str, name: str=None) -> None:
        """
        Parameters
        ----------
        name : str
            Name of the step.
        step_index : int
            The step number.
        step_type : str
            The type of the step can be any of 'initialization', 'characterization', 'degradation'.
        """

        allowable_step_types = ['initialization', 'characterization', 'degradation']
        if step_type not in allowable_step_types:
            raise ValueError("step_type must be one of the following: 'initialization', 'characterization', 'degradation'")
        self.name = name
        self.step_index = step_index
        self.step_type = step_type
        self.data_dict = {}
    
    def __str__(self) -> str:
        return f'ArbinStep name: {self.name}, step_index: {self.step_index}, step_type: {self.step_type}'

    def __getitem__(self, key: str) -> list:
        return self.data_dict[key]

    def __setitem__(self, key: str, value: list) -> None:
        self.data_dict[key] = value

    def get_data_as_array(self) -> np.array:
        """
        Returns
        -------
        ``numpy.ndarray``
            An array of the object attributes so that they form a table of step data.
        """
        return self.get_data_as_dataframe().to_numpy()

    def get_data_as_dataframe(self) -> pd.DataFrame:
        """
        Returns
        -------
        ``pandas.DataFrame``
            A table of the object data such that it replicates the input data csv.
        """
        return pd.DataFrame(self.data_dict)

    def plot_step_column(self, feature: str) -> plt.figure:
        """
        Plots the data for a given feature from this step.

        Parameters
        ----------
        ``feature`` \: ``str``
            Feature to be plotted such as Voltage(V). Must match a key in the 
            data_dict attribute of this ``ArbinStep``.
        """
        time_in_mins = np.array(self.data_dict['Step_Time(s)'])/60
        plt.plot(time_in_mins, self.data_dict[feature], label=f'step: {self.step_index}')
        plt.xlabel('Step Time (m)')
        plt.ylabel(feature)
        plt.legend()

class ArbinCycle:
    """
    Represents a cycle in a given test where any number of ``ArbinStep`` occur.

    Attributes
    ----------
    ``cycle_index`` \: ``int``
        The cycle number.
    ``steps`` \: ``list[ArbinStep]``
        List of ``ArbinStep`` in the cycle.
    ``name`` \: ``string``
        Name of the cycle. Default is ``''``.
    ``test_number`` \: ``int`` 
        The test number for the test that this cycle belongs too. Default is ``None``.

    Methods
    -------
    """
    
    def __init__(self, cycle_index: int, steps: list[ArbinStep]=[], name: str='', test_number: int=None) -> None:
        """
        Parameters
        ----------
        cycle_index : int
            The test cycle number.
        steps : list, optional
            List ArbinSteps in the test cycle.
        name : string, optional
            Name of the cycle.
        test_number : int, optional
            The test number for the test that this test cycle belongs too.
        """
        
        self.cycle_index = cycle_index
        self.steps = steps[:]
        self.name = name
        self.test_number = test_number

    def __str__(self) -> str:
        return f'ArbinCycle name: {self.name}, cycle_index: {self.cycle_index}, test number: {self.test_number}'

    def __iter__(self):
        self.iter_index = 0
        return self
        
    def __next__(self) -> ArbinStep:
        if self.iter_index < len(self.steps):
            step = self.steps[self.iter_index]
            self.iter_index += 1
            return step
        else:
            raise StopIteration
        
    def __getitem__(self, step_number) -> list[ArbinStep]:
        step_list = []
        if isinstance(step_number, int):
            for step in self.steps:
                if step.step_index == step_number:
                    step_list.append(step)
            if step_list:
                return step_list
            else:
                raise IndexError('No step with that step index.')
        elif isinstance(step_number, slice):
            range_start = 0
            range_stop = self._get_largest_index() + 1
            range_step = 1
            if step_number.start: range_start = step_number.start
            if step_number.stop: range_stop = step_number.stop
            if step_number.step: range_step = step_number.step
            
            for step in range(range_start, range_stop, range_step):
                # use try block to allow missing steps in range to be skipped.
                try:
                    step_list += self.get_step(step)
                except ValueError:
                    pass
            if step_list:
                return step_list
            else:
                raise IndexError('No steps within range')
            
    def __len__(self):
        return len(self.steps)

    def __del__(self):
        # Had to clear the step cache to fix a memory leak problem
        # It's my understanding that implementing __del__ isn't the 
        # best practice but I tried weakref's and it wasn't working
        self.steps.clear()

    def _get_largest_index(self) -> int:
        """
        Returns
        -------
        ``int``
            largest step index of all the step indices.
        """
        max_idx = 0
        for step in self.steps:
            if step.step_index > max_idx:
                max_idx = step.step_index
        return max_idx
    
    def add_step(self, step: ArbinStep) -> None:
        """
        Add a step to the list of steps in the cycle.

        Parameters
        ----------
        ``step`` \: ``ArbinStep``
            ``step`` to be added to the cycle.
        """
        self.steps.append(step)
    
    def get_step(self, step_number: int) -> list[ArbinStep | EisSweep]:
        """
        Gets arbin cycler steps matching the chosen step number in the cycle.

        Parameters
        ----------
        ``step_number`` \: ``int``
            Step index to be found.

        Returns
        -------
        ``list[ArbinStep]``
            List of steps within the cycle matching ``step_number``.
            Returns an empty list if there is no matches.
        """
        step_list = []
        for step in self.steps:
            if step.step_index == step_number\
                  and isinstance(step, (ArbinStep, EisSweep)):
                step_list.append(step)
        if step_list:
                return step_list
        else:
            raise ValueError('No step with that step index.')
    
    def get_eis_step(self, step_number: int) -> list[EisSweep]:
        """
        Gets gamry EIS steps matching the chosen step number in the cycle.

        Parameters
        ----------
        ``step_number`` \: ``int``
            Step index to be found.

        Returns
        -------
        ``list[EisSweep]``
            List of EIS steps within the cycle matching step_number.
            Returns an empty list if there is no matches.
        """
        step_list = []
        for step in self.steps:
            if step.step_index == step_number and isinstance(step, EisSweep):
                step_list.append(step)
        return step_list

class ArbinCell:
    """
    Represents a cell (battery) in a given test where any number of ``ArbinCycle`` occur.

    Attributes
    ----------
    ``cell_number`` \: ``int``
        Number assigned to the cell for the test.
    ``channel_number`` \: ``int``
        Channel assigned to the cell for the test.
    ``cycles`` \: ``list[ArbinCycle]``
        List of ``ArbinCycle``.
    ``headers`` \: ``list[str]``
        Name of column headers in the data. For example, Voltage(V).

    Methods
    -------
    """

    def __init__(self, cell_number: int, channel_number: int, cycles:list[ArbinCycle]=[], headers:list[str]=[]) -> None:
        """
        Parameters
        ----------
        cell_number : int
            Number assigned to the cell for the test.
        channel_number : int
            Channel assigned to the cell for the test.
        cycles : list[ArbinCycle]
            List of ArbinCycles that make up the test with keys equal to the cycle number.
        headers : list[str]
            Name of data values in the data file. For example, Voltage(V).
        """

        self.cell_number = cell_number
        self.channel_number = channel_number
        self.cycles = cycles[:]
        self.headers = headers

    def __str__(self) -> str:
        return f'ArbinCycle cell #: {self.cell_number}, channel #: {self.channel_number}'

    def __iter__(self):
        self.iter_index = 0
        return self
        
    def __next__(self) -> ArbinCycle:
        if self.iter_index < len(self.cycles):
            cycle = self.cycles[self.iter_index]
            self.iter_index += 1
            return cycle
        else:
            raise StopIteration

    def __getitem__(self, args) -> ArbinCycle:
        # returns a single cycle object
        if isinstance(args, int):
            return self.get_cycle(args)
        
        # returns a list of all cycle objects within
        # the range of the slice.
        elif isinstance(args, slice):
            range_start = 0
            range_stop = self._get_largest_index() + 1
            range_step = 1
            if args.start: range_start = args.start
            if args.stop: range_stop = args.stop
            if args.step: range_step = args.step
            
            cycle_list = []
            for cycle in range(range_start, range_stop, range_step):
                # use try block to allow missing steps in range to be skipped.
                try:
                    cycle_list.append(self.get_cycle(cycle))
                except ValueError:
                    pass
            if cycle_list:
                return cycle_list
            else:
                raise IndexError('No cycles within range')
        
        # returns a list of all step objects within the range
        # of the second slice within the cycles of the first slice.
        elif isinstance(args, tuple):
            if len(args) > 2:
                raise IndexError("Too many index arguments. Maximum is 2.")
            step_list = []
            if isinstance(args[0], int):
                cycle_list = [self[args[0]]]
            else:
                cycle_list = self[args[0]]
            for cycle in cycle_list:
                try:
                    step_list += cycle[args[1]]
                except IndexError:
                    # allow user to have empty cycles with in the range
                    # an error will only be thrown if ther is no steps
                    # in ANY of the cycles indexed.
                    pass
            if step_list:
                return step_list
            else:
                raise IndexError("No steps within range")
        else:
            raise TypeError("Invalid argument type.")
        
    def __len__(self):
        return len(self.cycles)


    def __del__(self):
        # Had to clear the cycle cache to fix a memory leak problem
        # It's my understanding that implementing __del__ isn't the 
        # best practice but I tried weakref's and it wasn't working
        self.cycles.clear()

    def _get_largest_index(self) -> int:
        """
        Returns
        -------
        ``int``
            largest step index of all the cycle indices.
        """
        max_idx = 0
        for cycle in self.cycles:
            if cycle.cycle_index > max_idx:
                max_idx = cycle.cycle_index
        return max_idx

    def add_cycle(self, cycle) -> None:
        """
        Add a cycle to the cell.

        Parameters
        ----------
        ``cycle`` \: ``ArbinCycle``
            ``ArbinCycle`` to be added to the object.
        """
        self.cycles.append(cycle)

    def update_headers(self, headers: list[str]) -> None:
        self.headers = headers

    def get_cycle(self, cycle_number: int) -> ArbinCycle:
        for cycle in self.cycles:
            if cycle.cycle_index == cycle_number:
                return cycle
        raise ValueError("Cycle number doesn't exist")