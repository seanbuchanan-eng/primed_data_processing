import os
from src.primed_data_processing.cellbuilder import CellBuilder
from src.primed_data_processing.arbin_cycler import ArbinCell, ArbinCycle, ArbinStep

def test_read_B6_csv_data():
    cellbuilder = CellBuilder()
    cell = ArbinCell(1, 1)

    directory = 'test/cycler_testing_data/'
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        cellbuilder.read_B6_csv_data(
            cell,
            directory + filename,
            {'characterization': [10,13,17],
             'degradation': [26,29,28]},
             verbose=False,
        )

    assert cell.headers == ['Date_Time',
                            'Test_Time(s)',
                            'Step_Time(s)',
                            'Step_Index',
                            'Cycle_Index',
                            'Voltage(V)',
                            'Current(A)',
                            'Charge_Capacity(Ah)',
                            'Discharge_Capacity(Ah)',
                            'Charge_Energy(Wh)',
                            'Discharge_Energy(Wh)',
                            'ACR(Ohm)',
                            'Internal Resistance(Ohm)',
                            'dV/dt(V/s)',
                            'Battery_Temperature(C)'
                            ]
    
    # check that step split between files import correctly
    assert cell.cycles[2].get_step(29)[-37]['Date_Time'][0] == '11/05/2021 01:08:17.148'
    assert cell.cycles[2].get_step(29)[-37]['Date_Time'][-1] == '11/05/2021 01:13:54.980'

    # check that type conversion worked
    assert type(cell.cycles[0].get_step(10)[0]['Date_Time'][0]) == str
    assert type(cell.cycles[0].get_step(10)[0]['Test_Time(s)'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['Step_Time(s)'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['Step_Index'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['Cycle_Index'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['Voltage(V)'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['Current(A)'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['Charge_Capacity(Ah)'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['Discharge_Capacity(Ah)'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['Charge_Energy(Wh)'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['Discharge_Energy(Wh)'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['ACR(Ohm)'][0]) == str
    assert type(cell.cycles[0].get_step(10)[0]['Internal Resistance(Ohm)'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['dV/dt(V/s)'][0]) == float
    assert type(cell.cycles[0].get_step(10)[0]['Battery_Temperature(C)'][0]) == float