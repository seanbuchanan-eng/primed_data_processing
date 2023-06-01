import pytest
import numpy as np
from src.primed_data_processing.gamry_eis import EisSweep

data_file = 'test/eis_testing_data/B6T10V0_Chan001_Cycle001_Step014.DTA'

def test_constructor():
    eis_sweep = EisSweep(f'eis cycle1', 0.5, 14)

    assert eis_sweep.soc == 0.5
    assert eis_sweep.name == 'eis cycle1'
    assert eis_sweep.step_index == 14
    assert eis_sweep.data_dict == {}

@pytest.fixture
def eis_sweep():
    return EisSweep(f'eis cycle1', 0.5, 14)

def test_methods(eis_sweep):
    eis_sweep.read_DTA_file(data_file)

    assert eis_sweep.soc == 0.5
    assert eis_sweep.name == 'eis cycle1'
    assert eis_sweep.step_index == 14
    assert eis_sweep._headers == ['Pt (#)','Time (s)','Freq (Hz)','Zreal (ohm)','Zimag (ohm)','Zsig (V)','Zmod (ohm)','Zphz (degrees)','Idc (A)','Vdc (V)', 'IERange (#)']
    
    # test data dict
    assert eis_sweep.data_dict['Pt (#)'] == [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    assert eis_sweep.data_dict['Time (s)'] == [1,2,4,5,6,7,9,10,11,12,14,15,16,18,21,24]
    assert eis_sweep.data_dict['Freq (Hz)'] == [100019.5,46464.84,21621.09,10019.53,4630.335,2141.204,1000.702,463.5989,215.0229,99.734,45.95588,21.50229,9.9734,4.650298,2.170139,0.997765]
    assert eis_sweep.data_dict['Zreal (ohm)'] == [0.0229291,0.0162025,0.011836,0.0093414,0.0084784,0.0085059,0.0089637,0.0097023,0.0106352,0.0116262,0.0124733,0.0130281,0.013348,0.0135265,0.0136656,0.0138303]
    assert eis_sweep.data_dict['Zimag (ohm)'] == [-0.0030148,0.0022876,0.0034139,0.0023389,0.0008887,-0.0001959,-0.0009269,-0.001413,-0.0016568,-0.0016203,-0.0013285,-0.0009596,-0.0006621,-0.0005055,-0.0004833,-0.0006665]
    assert eis_sweep.data_dict['Zsig (V)'] == [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    assert eis_sweep.data_dict['Zmod (ohm)'] == [0.0231264,0.0163632,0.0123185,0.0096298,0.0085248,0.0085082,0.0090115,0.0098047,0.0107635,0.0117386,0.0125438,0.0130634,0.0133644,0.0135359,0.0136741,0.0138464]
    assert eis_sweep.data_dict['Zphz (degrees)'] == [-7.490437,8.036185,16.08913,14.05653,5.983749,-1.31953,-5.903959,-8.28618,-8.854591,-7.933879,-6.079385,-4.212512,-2.839614,-2.140391,-2.025336,-2.759135]
    assert eis_sweep.data_dict['Idc (A)'] == [0.0018029,0.0019511,0.0020157,0.0020214,0.0016092,0.0015952,0.0016182,0.0015795,0.0015841,0.0015549,0.0016273,0.0016696,0.0016631,0.001661,0.0017331,0.0017134]
    assert eis_sweep.data_dict['Vdc (V)'] == [3.760538,3.760587,3.760552,3.760539,3.760588,3.760565,3.760558,3.760599,3.760582,3.760585,3.76058,3.760617,3.760635,3.760644,3.760725,3.760797]
    assert eis_sweep.data_dict['IERange (#)'] == [12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12]

    # test __getitem__
    assert eis_sweep['Pt (#)'] == [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    assert eis_sweep['Time (s)'] == [1,2,4,5,6,7,9,10,11,12,14,15,16,18,21,24]
    assert eis_sweep['Freq (Hz)'] == [100019.5,46464.84,21621.09,10019.53,4630.335,2141.204,1000.702,463.5989,215.0229,99.734,45.95588,21.50229,9.9734,4.650298,2.170139,0.997765]
    assert eis_sweep['Zreal (ohm)'] == [0.0229291,0.0162025,0.011836,0.0093414,0.0084784,0.0085059,0.0089637,0.0097023,0.0106352,0.0116262,0.0124733,0.0130281,0.013348,0.0135265,0.0136656,0.0138303]
    assert eis_sweep['Zimag (ohm)'] == [-0.0030148,0.0022876,0.0034139,0.0023389,0.0008887,-0.0001959,-0.0009269,-0.001413,-0.0016568,-0.0016203,-0.0013285,-0.0009596,-0.0006621,-0.0005055,-0.0004833,-0.0006665]
    assert eis_sweep['Zsig (V)'] == [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    assert eis_sweep['Zmod (ohm)'] == [0.0231264,0.0163632,0.0123185,0.0096298,0.0085248,0.0085082,0.0090115,0.0098047,0.0107635,0.0117386,0.0125438,0.0130634,0.0133644,0.0135359,0.0136741,0.0138464]
    assert eis_sweep['Zphz (degrees)'] == [-7.490437,8.036185,16.08913,14.05653,5.983749,-1.31953,-5.903959,-8.28618,-8.854591,-7.933879,-6.079385,-4.212512,-2.839614,-2.140391,-2.025336,-2.759135]
    assert eis_sweep['Idc (A)'] == [0.0018029,0.0019511,0.0020157,0.0020214,0.0016092,0.0015952,0.0016182,0.0015795,0.0015841,0.0015549,0.0016273,0.0016696,0.0016631,0.001661,0.0017331,0.0017134]
    assert eis_sweep['Vdc (V)'] == [3.760538,3.760587,3.760552,3.760539,3.760588,3.760565,3.760558,3.760599,3.760582,3.760585,3.76058,3.760617,3.760635,3.760644,3.760725,3.760797]
    assert eis_sweep['IERange (#)'] == [12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12]

    # check visually to ensure correctness
    df = eis_sweep.get_data_as_dataframe()
    
    arr = eis_sweep.get_data_as_array()
    assert arr.shape == (16,11)
    
