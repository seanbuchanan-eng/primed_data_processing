import pytest
import numpy as np
from primed_data_processing.cellbuilder import CellBuilder
from primed_data_processing.arbin_cycler import ArbinBatch, ArbinCell, ArbinCycle, ArbinStep

cell_builder = CellBuilder()
datapath1 = 'test/cycler_testing_data/B6T10V0_1_2_3_4_9_10_11_12_13_14_15_16_Channel_1.1.csv'
datapath2 = 'test/cycler_testing_data/B6T10V0_1_2_3_4_9_10_11_12_13_14_15_16_Channel_1.2.csv'
steps = {
    'characterization': [6,7,10],
    'degradation': [25]
}

@pytest.fixture
def cell():
    cell = ArbinCell(cell_number=1, channel_number=1)
    cell_builder.read_B6_csv_data(cell=cell, file_path=datapath1, steps=steps)
    return cell

@pytest.fixture
def batch(cell):
    cell2 = ArbinCell(cell_number=2, channel_number=2)
    cell_builder.read_B6_csv_data(cell=cell2, file_path=datapath2, steps=steps)
    return ArbinBatch(cells=[cell, cell2])

def test_cell_indexing(cell):
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

def test_batch_indexing(batch):
    # single cycle
    assert isinstance(batch[1], ArbinCell)
    assert batch[1].cell_number == 1

    # cell slice
    assert isinstance(batch[1:3], list)
    assert len(batch[1:3]) == 2
    cell_nums = [1,2]
    for idx, cell in enumerate(batch[1:3]):
        assert cell.cell_number == cell_nums[idx]
        assert isinstance(cell, ArbinCell)

    # multislice: single cell, single cycle
    assert isinstance(batch[2,3], list)
    for cycle in batch[2,3]:
        assert cycle.cycle_index == 3
        assert isinstance(cycle, ArbinCycle)

    # multislice: cell slice, single cycle
    for cycle in batch[1:3,4]:
        assert cycle.cycle_index == 4
        assert isinstance(cycle, ArbinCycle)

    # multislice: cell slice, cycle slice
    cycle_nums = [3,4,5]
    for cycle in batch[1:,3:6]:
        assert cycle.cycle_index in cycle_nums
        assert isinstance(cycle, ArbinCycle)

    # test different step slicing permutations
    step_nums = [6,7,10,25]
    for step in batch[:,:,:]:
        assert step.step_index in step_nums
        assert isinstance(step, ArbinStep)

    for step in batch[:2,:3,6]:
        assert step.step_index == 6
        assert isinstance(step, ArbinStep)

    for step in batch[2:,3:,7:11]:
        assert step.step_index in step_nums
        assert isinstance(step, ArbinStep)

    for step in batch[1,3,:7]:
        assert step.step_index == 6
        assert isinstance(step, ArbinStep)

    for step in batch[2,5,7:]:
        assert step.step_index in step_nums
        assert isinstance(step, ArbinStep)


def test_iter(batch):
    cell_count = 0
    cycle_count = 0
    step_count = 0
    for cell in batch:
        cell_count += 1
        assert isinstance(cell, ArbinCell)
        for cycle in cell:
            cycle_count += 1
            assert isinstance(cycle, ArbinCycle)
            for step in cycle:
                step_count += 1
                assert isinstance(step, ArbinStep)
    assert cell_count > 0
    assert cycle_count > 0
    assert step_count > 0

# TODO test batch indexing
