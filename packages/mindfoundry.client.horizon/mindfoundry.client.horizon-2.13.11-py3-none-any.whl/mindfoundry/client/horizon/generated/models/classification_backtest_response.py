from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.classification_backtest_insight import ClassificationBacktestInsight

T = TypeVar("T", bound="ClassificationBacktestResponse")


@attr.s(auto_attribs=True)
class ClassificationBacktestResponse:
    """  """

    insight: ClassificationBacktestInsight
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        insight = self.insight.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "insight": insight,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        insight = ClassificationBacktestInsight.from_dict(d.pop("insight"))

        classification_backtest_response = cls(
            insight=insight,
        )

        classification_backtest_response.additional_properties = d
        return classification_backtest_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
