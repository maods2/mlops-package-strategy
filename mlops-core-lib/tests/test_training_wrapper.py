import pytest

from mlops_core_lib.interfaces import TrainingWrapper


def test_training_wrapper_contract_enforced() -> None:
    with pytest.raises(TypeError):
        TrainingWrapper()
