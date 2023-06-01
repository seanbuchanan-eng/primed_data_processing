# Sean Buchanan
# This module contains classes that can be used to process and store EIS data
# for ease of use.

import numpy as np
import pandas as pd

class EisSweep:
    """
    Represents a single EIS sweep.

    An EIS sweep is a sweep from some start frequency to some end frequency with a 
    specified number of data points within each frequency decade. The sweep occurs
    at a specified SOC.

    Attributes
    ----------
    ``name`` \: ``str``
        Name of the eis sweep.
    ``soc`` \: ``float``
        State-of-charge of battery when eis measurement was taken. 0 <= soc <=1.
    ``step_index`` \: ``int``
        Index of the EIS step in the arbin test schedule. Default is 0.
    ``pt`` \: ``list[int]``
        Point numbers of the measurements.
    ``time`` \: ``list[float]``
        Duration of the measurements in seconds.
    ``freq`` \: ``list[float]``
        Frequency of the measurements in Hz.
    ``z_real`` \: ``list[float]``
        Real portion of the batteries measured impedance response in Ohms.
    ``z_imag`` \: ``list[float]``
        Imaginary portion of the batteries measured impedance response in Ohms.
    ``z_sig`` \: ``list[float]``
        Measured in Volts.
    ``z_mod`` \: ``list[float]``
        Magnitude of the batteries measured impedance response in Ohms.
    ``z_phase`` \: ``list[float]``
        Phase of the batteries measured impedance response in degrees.
    ``idc`` \: ``list[float]``
        Measured DC current in Amps.
    ``vdc`` \: ``list[float]``
        Measured DC voltage in Volts.
    ``ie_reange`` \: ``list[int]``
        Not sure. For now it is just a column in the Gamry DTA file.
        
    Methods
    -------
    """

    def __init__(self, name: str, soc: float, step_index: int=0) -> None:
        """
        Parameters
        ----------
        ``name`` \: ``str``
            Name of the EisSweep
        ``soc`` \: ``float``
            State-of-charge of battery when eis measurement was taken. 0 <= ``soc`` <=1
        ``step_index`` \: ``int`` optional, default is 0
            Index of the EIS step in the arbin test schedule.
        """
        self.name = name
        self.soc = soc
        self.step_index = step_index
        self.data_dict = {}
        self._data_already_read = False

    def __str__(self):
        return f'EisSweep object name: {self.name}, soc: {self.soc}, step_index: {self.step_index}'
    
    def __getitem__(self, key: str) -> list:
        return self.data_dict[key]

    def __setitem__(self, key: str, value: list) -> None:
        self.data_dict[key] = value

    def read_DTA_file(self, file_path: str) -> None:
        """
        Read a Gamry DTA output file and store its information in this ``EisSweep`` object.

        Parameters
        ----------
        ``file_path`` \: ``str``
            Absolute path to the Gamry DTA file.
        """
        if self._data_already_read:
            raise ValueError('Data has already been read for this object! Either delete or make a new object.')

        with open(file_path) as file:
            read = False
            for line in file:
                if line.startswith('	Pt'):
                    self._headers = line.split()
                elif line.startswith('	#'):
                    units = line.split()
                    for idx, header in enumerate(self._headers):
                        # remove degree symbol from phz header
                        if header == 'Zphz':
                            self._headers[idx] = 'Zphz (degrees)'
                        else:
                            self._headers[idx] = header + ' (' + units[idx] + ')'
                    for header in self._headers:
                        self.data_dict[header] = []
                elif line.startswith('	0'):
                   read = True
                if read == True:
                    data = line.split()
                    self.data_dict[self._headers[0]].append(int(data[0]))
                    self.data_dict[self._headers[1]].append(float(data[1]))
                    self.data_dict[self._headers[2]].append(float(data[2]))
                    self.data_dict[self._headers[3]].append(float(data[3]))
                    self.data_dict[self._headers[4]].append(float(data[4]))
                    self.data_dict[self._headers[5]].append(float(data[5]))
                    self.data_dict[self._headers[6]].append(float(data[6]))
                    self.data_dict[self._headers[7]].append(float(data[7]))
                    self.data_dict[self._headers[8]].append(float(data[8]))
                    self.data_dict[self._headers[9]].append(float(data[9]))
                    self.data_dict[self._headers[10]].append(int(data[10]))

        self._data_already_read = True

    def get_data_as_array(self) -> np.array:
        """
        Returns
        -------
        ``numpy.ndarray``
            Nx11 array where the columns are pt, time, freq, zreal, zimag, zsig, zmod,
            zphase, idc, vdc, ierange
        """
        return self.get_data_as_dataframe().to_numpy()

    def get_data_as_dataframe(self) -> pd.DataFrame:
        """
        Returns
        -------
        ``pandas.DataFrame``
            Nx11 table where column headers are pt, time, freq, zreal, zimag, zsig,
            zmod, zphase, idc, vdc, ierange
        """
        return pd.DataFrame(self.data_dict)

class EisCycle:
    """
    Represents a cycle in a given test where any number of ``EisSweep`` can occur.

    Attributes
    ----------
    ``cycle_number`` \: ``int``
        The cycle number in the test.
    ``sweeps`` \: ``list[EisSweep]``
        List of ``EisSweep`` objects that occur in this cycle.
    ``name`` \: ``str`` optional, default is ``''``
        Name of the object.

    Methods
    -------
    """
    
    def __init__(self, cycle_number: int, sweeps: list[EisSweep]=[], name='') -> None:
        """
        Parameters
        ----------
        ``cycle_number`` : ``int``
            The cycle number in the test.
        ``sweeps`` : ``list[EisSweep]`` optional, default is ``[]``
            List of ``EisSweep`` objects. It is recommended to put them in chronological order.
        ``name`` : ``str`` optional, default is ``''``
            Name of the object.
        """

        self.cycle_index = cycle_number
        self.sweeps = sweeps
        self.name = name

    def __str__(self) -> str:
        return f'EisCycle name: {self.name}, cycle index: {self.cycle_index}'

    def __iter__(self):
        self.iter_index = 0
        return self
        
    def __next__(self) -> EisSweep:
        if self.iter_index < len(self.sweeps):
            eis_sweep = self.sweeps[self.iter_index]
            self.iter_index += 1
            return eis_sweep
        else:
            raise StopIteration

    def __getitem__(self, idx: int) -> EisSweep:
        return self.sweeps[idx]

    def add_sweep(self, eis_sweep) -> None:
        """
        Add an ``EisSweep`` object to the cycle.

        Parameters
        ----------
        ``eis_sweep`` \: ``EisSweep``
            ``EisSweep`` object to be added to the cycle.
        """
        self.sweeps.append(eis_sweep)

    def get_data_as_array(self) -> np.array:
        """
        Returns
        -------
        ``numpy.ndarray``
            All EisSweeps in the cycle as a m x n x 11 array where m is the number of sweeps, n is the 
            number of measurements, and 11 is the number of columns.

            Can also be seen as an output of m ``EisSweep.get_data_as_array()``.
        """
        output_list = []
        for eis_sweep in self.sweeps:
            output_list.append(eis_sweep.get_data_as_array())
        
        return np.array(output_list)

class EisCell:
    """
    Represents a cell (battery) in a given test where any number of ``EisCycle`` can occur.

    Attributes
    ----------
    ``name`` \: ``str``
        Name of the cell. Default is ``''``.
    ``eis_cycles`` \: ``list[EisCycle]``
        List of ``EisCycle`` objects representing all of the sweeps measured in a given cycle.
    ``cell_number`` \: ``int``
        The cell number from the test.
    ``channel_number`` \: ``int``
        The channel number from the test.

    Methods
    -------
    """

    def __init__(self, cell_number, channel_number, name='', eis_cycles=[]) -> None:
        """
        Parameters
        ----------
        name : str, optional default is ''.
            Name of the cell. 
        eis_cycles : list, optional
            EisCycle objects representing all of the sweeps measured in a given cycle 9def.
        cell_number : int
            The cell number from the test.
        channel_number : int
            The channel number from the test.
        """
        self.name = name
        self.cycles = eis_cycles
        self.cell_number = cell_number
        self.channel_number = channel_number

    def __str__(self):
        return f'EisCell name: {self.name}, cell #: {self.cell_number}, channel # {self.channel_number}'

    def __iter__(self):
        self.iter_index = 0
        return self
        
    def __next__(self) -> EisSweep:
        if self.iter_index < len(self.cycles):
            eis_cycle = self.cycles[self.iter_index]
            self.iter_index += 1
            return eis_cycle
        else:
            raise StopIteration

    def __getitem__(self, idx: int) -> EisCycle:
        return self.cycles[idx]

    def add_cycle(self, eis_cycle) -> None:
        """
        Parameters
        ----------
        ``eis_cycle`` \: ``EisCycle``
            ``EisCycle`` to be added to the cell.
        """
        self.cycles.append(eis_cycle)

    def get_data_as_array(self) -> np.array:
        """
        Returns
        -------
        ``numpy.ndarray``
            All ``EisCycles`` in the cell. Shape is z x m x n x 11 where z is the number
            of cycles, m is the number of sweeps, and n is the number of data points in the sweep. 11 is
            the number of measured parameters in the EIS sweep.
        """
        output_list = []
        for eis_cycle in self.cycles:
            output_list.append(eis_cycle.get_data_as_array())
        
        return np.array(output_list)
