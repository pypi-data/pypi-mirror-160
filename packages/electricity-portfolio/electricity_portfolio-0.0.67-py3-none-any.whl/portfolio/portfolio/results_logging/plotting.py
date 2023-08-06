from dataclasses import dataclass
from typing import List

from portfolio.resources.technologies import Asset


@dataclass
class StackPlotConfig:
    plot: bool
    line_plot_order: List[str]
    color_map: dict
    stack_plot_order: List[str]
