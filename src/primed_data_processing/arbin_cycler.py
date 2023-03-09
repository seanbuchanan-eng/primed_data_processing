# Sean Buchanan
# This module is intended to be an easy to use datastructure for
# Arbin battery data produced at PRIMED.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.primed_data_processing.gamry_eis import EisCell, EisSweep

class ArbinStep:
    """
    Represents a step in an Arbin MITS PRO test schedule.

    Attributes
    ----------

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

    def __getitem__(self, key: str) -> list:
        return self.data_dict[key]

    def __setitem__(self, key: str, value: list) -> None:
        self.data_dict[key] = value

    def get_data_as_array(self) -> np.array:
        """
        Returns
        -------
        numpy array
            An array of the object attributes so that they form a table of step data.
        """
        pass

    def get_data_as_dataframe(self) -> pd.DataFrame:
        """
        Returns
        -------
        pandas DataFrame
            A table of the object data such that it replicates the input csv.
        """
        return pd.DataFrame(self.data_dict)

    def plot_step_column(self, feature: str) -> plt.figure:
        time_in_mins = np.array(self.data_dict['Step_Time(s)'])/60
        plt.plot(time_in_mins, self.data_dict[feature], label=f'step: {self.step_index}')
        plt.xlabel('Step Time (m)')
        plt.ylabel(feature)
        plt.legend()

class ArbinTestCycle:
    """
    Represents a full Arbin test cycle.

    This object is built with various different ArbinSteps.

    Attributes
    ----------

    Methods
    -------
    """
    
    def __init__(self, cycle_index: int, steps: list[ArbinStep]=[], name: str=None, test_number: int=None) -> None:
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
        for step in self.steps:
            if step.step_index == step_number:
                step_list.append(step)
        if step_list:
            return step_list
        else:
            raise ValueError('No step with that step index!')
        

    def __del__(self):
        # Had to clear the step cache to fix a memory leak problem
        # It's my understanding that implementing __del__ isn't the 
        # best practice but I tried weakref's and it wasn't working
        self.steps.clear()

    def add_step(self, step: ArbinStep) -> None:
        """
        Parameters
        ----------
        step : ArbinStep
            step to be added to the cycle.
        """
        self.steps.append(step)
    
    def get_step(self, step_number: int) -> list[ArbinStep]:
        """
        Gets arbin steps matching the chosen step number in the cycle.

        Parameters
        ----------
        step_number : int
            step index to be found

        Returns
        -------
        list[ArbinStep]
            list of steps within the cycle matching step_number.
            Returns an empty list if there is no matches.
        """
        step_list = []
        for step in self.steps:
            if step.step_index == step_number and isinstance(step, ArbinStep):
                step_list.append(step)
        return step_list
    
    def get_eis_step(self, step_number: int) -> list[EisSweep]:
        """
        Gets gamry steps matching the chosen step number in the cycle.

        Parameters
        ----------
        step_number : int
            step index to be found

        Returns
        -------
        list[ArbinStep]
            list of steps within the cycle matching step_number.
            Returns an empty list if there is no matches.
        """
        step_list = []
        for step in self.steps:
            if step.step_index == step_number and isinstance(step, EisSweep):
                step_list.append(step)
        return step_list


class ArbinCell:
    """
    Represents an entire test for a single battery (cell).

    Attributes
    ----------

    Methods
    -------
    """

    def __init__(self, cell_number: int, channel_number: int, cycles:ArbinTestCycle=[], headers:str=[]) -> None:
        """
        Parameters
        ----------
        cell_number : int
            Number assigned to the cell for the test.
        channel_number : int
            Channel assigned to the cell for the test.
        cycles : dict
            Dictionary of ArbinTestCycles that make up the test with keys equal to the cycle number.
        """

        self.cell_number = cell_number
        self.channel_number = channel_number
        self.cycles = cycles[:]
        self.headers = headers

    def __iter__(self):
        self.iter_index = 0
        return self
        
    def __next__(self) -> ArbinTestCycle:
        if self.iter_index < len(self.cycles):
            cycle = self.cycles[self.iter_index]
            self.iter_index += 1
            return cycle
        else:
            raise StopIteration

    def __getitem__(self, cycle_number) -> ArbinTestCycle:
        if isinstance(cycle_number, int):
            for cycle in self.cycles:
                if cycle.cycle_index == cycle_number:
                    return cycle
        else:
            raise TypeError("Invalid argument type.")

    def __del__(self):
        # Had to clear the cycle cache to fix a memory leak problem
        # It's my understanding that implementing __del__ isn't the 
        # best practice but I tried weakref's and it wasn't working
        self.cycles.clear()

    def add_cycle(self, cycle) -> None:
        """
        Add a cycle to the test.

        Parameters
        ----------
        cycle : ArbinTestCycle
            Cycle to be added to the object.
        """
        self.cycles.append(cycle)

    def update_headers(self, headers: list) -> None:
        self.headers = headers

    def get_cycle(self, cycle_number: int) -> ArbinTestCycle:
        return self[cycle_number]