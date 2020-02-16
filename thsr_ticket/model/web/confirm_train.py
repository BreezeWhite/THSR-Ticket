from typing import Mapping, Any
from jsonschema import validate

from thsr_ticket.model.web.abstract_params import AbstractParams
from thsr_ticket.configs.web.param_schema import CONFIRM_TRAIN_SCHEMA


class ConfirmTrain(AbstractParams):
    def __init__(self) -> None:
        super(ConfirmTrain, self).__init__()
        self._selection: str = None

    def get_params(self, val: bool = True) -> Mapping[str, Any]:
        params = {
            "BookingS2Form:hf:0": "",
            "TrainQueryDataViewPanel:TrainGroup": self._selection
        }

        if val:
            validate(params, schema=CONFIRM_TRAIN_SCHEMA)
        return params

    @property
    def selection(self) -> str:
        return self._selection

    @selection.setter
    def selection(self, value: str) -> None:
        if not value.startswith("radio"):
            raise ValueError("Wrong prefix. Should start with 'radio', given: {}".format(value))
        self._selection = value
