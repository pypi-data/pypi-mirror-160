from typing import Any

import dimod
import jijmodeling as jm

from jijmodeling.sampleset import Evaluation, MeasuringTime, Parameters, Record

from jijzept.response.base import BaseResponse


class JijModelingResponse(BaseResponse, jm.SampleSet):
    @classmethod
    def from_json_obj(cls, json_obj) -> Any:
        if "type" in json_obj.keys():
            response = cls.from_dimod_response(json_obj)
        else:
            response = cls.from_serializable(json_obj)
        return response

    @classmethod
    def empty_data(cls) -> Any:
        return cls(
            record=Record({"x": []}, [0]),
            evaluation=Evaluation([]),
            measuring_time=MeasuringTime(),
            best_parameters=Parameters(),
        )

    @classmethod
    def from_dimod_response(cls, json_obj):
        sampleset = cls.from_dimod_sampleset(
            dimod.SampleSet.from_serializable(json_obj)
        )
        return cls(
            record=sampleset.record,
            evaluation=sampleset.evaluation,
            measuring_time=sampleset.measuring_time,
            best_parameters=sampleset.best_parameters,
        )

    def __repr__(self):
        return jm.SampleSet.__repr__(self)

    def __str__(self):
        return BaseResponse.__repr__(self) + "\n" + jm.SampleSet.__str__(self)
