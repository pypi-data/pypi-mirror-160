from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.dataset import Dataset
from ..models.ingestion_process import IngestionProcess

T = TypeVar("T", bound="AllDatasets")


@attr.s(auto_attribs=True)
class AllDatasets:
    """  """

    datasets: List[Dataset]
    ingestion_processes: List[IngestionProcess]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datasets = []
        for datasets_item_data in self.datasets:
            datasets_item = datasets_item_data.to_dict()

            datasets.append(datasets_item)

        ingestion_processes = []
        for ingestion_processes_item_data in self.ingestion_processes:
            ingestion_processes_item = ingestion_processes_item_data.to_dict()

            ingestion_processes.append(ingestion_processes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datasets": datasets,
                "ingestionProcesses": ingestion_processes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        datasets = []
        _datasets = d.pop("datasets")
        for datasets_item_data in _datasets:
            datasets_item = Dataset.from_dict(datasets_item_data)

            datasets.append(datasets_item)

        ingestion_processes = []
        _ingestion_processes = d.pop("ingestionProcesses")
        for ingestion_processes_item_data in _ingestion_processes:
            ingestion_processes_item = IngestionProcess.from_dict(ingestion_processes_item_data)

            ingestion_processes.append(ingestion_processes_item)

        all_datasets = cls(
            datasets=datasets,
            ingestion_processes=ingestion_processes,
        )

        all_datasets.additional_properties = d
        return all_datasets

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
