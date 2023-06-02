import pytest
import numpy as np
from primed_data_processing.cellbuilder import CellBuilder
from primed_data_processing.arbin_cycler import ArbinCell, ArbinCycle, ArbinStep

cell_builder = CellBuilder()
datapath = 'test/cycler_testing_data/B6T10V0_1_2_3_4_9_10_11_12_13_14_15_16_Channel_1.1.csv'

@pytest.fixture
def cell():
    steps = {
    'characterization': [6,7,10],
    'degradation': [25]
    }
    cell = ArbinCell(cell_number=1, channel_number=1)
    cell_builder.read_B6_csv_data(cell=cell, file_path=datapath, steps=steps)
    return cell

def test_indexing(cell):
    # single cycle
    assert isinstance(cell[1], ArbinCycle)
    assert cell[1].cycle_index == 1

    # cycle slice
    assert isinstance(cell[1:4], list)
    assert len(cell[1:4]) == 3
    cycle_nums = [1,2,3]
    for idx, cycle in enumerate(cell[1:4]):
        assert cycle.cycle_index == cycle_nums[idx]
        assert isinstance(cycle, ArbinCycle)

    # multislice: single cycle, single step
    assert isinstance(cell[3,10], list)
    for step in cell[3,10]:
        assert step.step_index == 10
        assert isinstance(step, ArbinStep)

    # multislice: cycle slice, single step
    for step in cell[1:4,10]:
        assert step.step_index == 10
        assert isinstance(step, ArbinStep)

    # multislice: cycle slice, step slice
    step_nums = [6,7,10]
    for step in cell[1:, 6:11]:
        assert step.step_index in step_nums
        assert isinstance(step, ArbinStep)

    # test different slicing permutations
    step_nums = [6,7,10,25]
    for step in cell[:,2:]:
        assert step.step_index in step_nums
        assert isinstance(step, ArbinStep)

    for step in cell[:3, :7]:
        assert step.step_index == 6
        assert isinstance(step, ArbinStep)

    for step in cell[5, :]:
        assert step.step_index in step_nums
        assert isinstance(step, ArbinStep)

# def test_arbin_step(cell):
#     # get step 10 in cycle 1
#     step = cell[1,10]
