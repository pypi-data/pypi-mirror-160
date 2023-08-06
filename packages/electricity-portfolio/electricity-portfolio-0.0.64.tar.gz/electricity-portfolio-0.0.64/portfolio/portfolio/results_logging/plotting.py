from dataclasses import dataclass
from typing import List

from portfolio.resources.technologies import Asset


@dataclass
class StackPlotConfig:
    plot: bool
    color_map: dict
    plot_order: List[str]
