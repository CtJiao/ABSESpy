#!/usr/bin/env python 3.11.0
# -*-coding:utf-8 -*-
# @Author  : Shuang (Twist) Song
# @Contact   : SongshGeo@gmail.com
# GitHub   : https://github.com/SongshGeo
# Website: https://cv.songshgeo.com/

from abses import MainModel
from abses.time import time_condition
from examples.water_quota.yr_human import Society
from examples.water_quota.yr_nature import Nature


class YellowRiver(MainModel):
    """模拟黄河的水资源分配"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            self, nature_class=Nature, human_class=Society, *args, **kwargs
        )

    @property
    def institution(self) -> str | None:
        """黄河流域的制度"""
        if self.time.year <= 1987:
            return None
        if self.time.year <= 1998:
            return "87-WAS"
        if self.time.year <= 2008:
            return "98-UBR"
        raise ValueError(f"{self.time.year} exceed the study period.")

    @time_condition({"month": 12})
    def update_scores(self):
        """更新得分"""
        farmers = self.agents.select("Farmer")
        payoff = farmers.array("s") * farmers.array("e")
        farmers.update("payoff", payoff)

    def step(self):
        self.nature.step()
        self.human.step()
        self.update_scores()
