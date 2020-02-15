import pytest
import jsonschema

from thsr_ticket.model.web.confirm_train import ConfirmTrain

train = ConfirmTrain()


@pytest.mark.parametrize("val", ["wrong_prefix", "hahaha"])
def test_selection(val):
    with pytest.raises(ValueError):
        train.selection = val


def test_get_params():
    expected = {
        "BookingS2Form:hf:0": "",
        "TrainQueryDataViewPanel:TrainGroup": "radio21"
    }

    with pytest.raises(jsonschema.exceptions.ValidationError):
        train.get_params()

    train.selection = "radio21"
    assert train.selection == "radio21"
    assert train.get_params() == expected
