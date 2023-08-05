from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="AlgoExecutionDataFeaturehistory")


@attr.s(auto_attribs=True)
class AlgoExecutionDataFeaturehistory:
    """ Recent values for all assets. Key = asset name. Value = list of recent values """

    additional_properties: Dict[str, List[float]] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        algo_execution_data_featurehistory = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = cast(List[float], prop_dict)

            additional_properties[prop_name] = additional_property

        algo_execution_data_featurehistory.additional_properties = additional_properties
        return algo_execution_data_featurehistory

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> List[float]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: List[float]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
