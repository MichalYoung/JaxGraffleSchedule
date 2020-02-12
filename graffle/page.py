""""
Generic support (abstract classes) for chart graphics.
Specific output media, like OmniGraffle or SVG, should
provide concrete subclasses with implementations that
fill in some missing parts.

Prototype version includes the OmniGraffle JXA
implementation for ease of development; this should
move when it is basically working.
"""

import sys
from typing import Tuple, List
import numbers.Number as Number

class Point:
    def __init__(self, x: Number, y: Number):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if isinstance(other, number):
            """Scale"""
            return Point(other * self.x, other * self.y)
        elif isinstance(other, Point):
            """Dot product (scalar inner product)"""
            return self.x * other.x + self.y + other.y
        else:
            raise ValueError(f"Multiplication not defined for {self.__class__} * {other.__class__}")

class Device:
    """Abstract base class for specific output formats"""
    def __init__(self):
        raise NotImplementedError("'Device' is an abstract class")

    def line(self, x0: Number, y0: Number, x1: Number, y1: Number, label="", style=none):
        raise NotImplementedError(f"{self._class_} has no implementation of 'line'")

    def rect(self, x0, y0, x1, y1, label="", style=None):
        raise NotImplementedError(f"{self._class_} has no implementation of 'rect'")


class Grid:
    """We view the page through a grid with integral columns
    and potentially non-integral rows (i.e., things can be from
    row 1.5 to row 2.7 in column 3).  Rows and columns are numbered
    from zero.
    """
    def __init__(self,
                 extent: Tuple[Tuple[Number, Number], Tuple[Number, Number]] = ((0,0) , (100,100)),
                 sfx: Number=1.0, sfy: Number=1.0,
                 columns: List[Number] = [1]):
        self.extent = extent   # (x,y) upper left to (x,y) lower right
        self.columns = columns
        # Redundant breakout of extent so that I don't need to repeat
        # the code in other methods.
        upper_left, lower_right = extent
        self.ul_x, self.ul_y = upper_left
        self.lr_x, self.lr_y = lower_right
        # The columns are given in terms of relative size, e.g.,
        # columns [1, 2, 1] would have widths 0.25*(lr_x-ul_x),
        # 0.5*(lr_x-ul_x), 0.25*(lr_x-ul_x).  We record this in
        # self.columns as a list of (left, scale) pairs
        pagewidth = lr_x - ul_x
        col_sum = sum(columns)
        self.columns = []
        left = 0.0
        for col in columns:
            col_width = pagewidth * (col / col_sum)
            self.columns.append((left, col_width))
            left += col_width


    def tx(self, col: int, row: Number) -> Tuple[Number, Number]:
       """Transform to device coordinates"""
       # The input point is (column, row), where column
       # should be an integer and
       if not isinstance(col, int) or col < 0 or col >= len(self.columns):
           raise ValueError("col must be integer in 0..n_columns")
       x_left, x_scale = self.columns[col]
       x = x_left

        ulx, uly = upper_left
        x, y = pt
        return










