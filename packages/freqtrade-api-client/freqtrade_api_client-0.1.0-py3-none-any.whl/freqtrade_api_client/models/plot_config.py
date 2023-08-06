from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.plot_config_main_plot import PlotConfigMainPlot
from ..models.plot_config_subplots import PlotConfigSubplots

T = TypeVar("T", bound="PlotConfig")


@attr.s(auto_attribs=True)
class PlotConfig:
    """
    Attributes:
        main_plot (PlotConfigMainPlot):
        subplots (PlotConfigSubplots):
    """

    main_plot: PlotConfigMainPlot
    subplots: PlotConfigSubplots
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        main_plot = self.main_plot.to_dict()

        subplots = self.subplots.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "main_plot": main_plot,
                "subplots": subplots,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        main_plot = PlotConfigMainPlot.from_dict(d.pop("main_plot"))

        subplots = PlotConfigSubplots.from_dict(d.pop("subplots"))

        plot_config = cls(
            main_plot=main_plot,
            subplots=subplots,
        )

        plot_config.additional_properties = d
        return plot_config

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
