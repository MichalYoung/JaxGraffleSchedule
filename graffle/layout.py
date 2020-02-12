"""
Generate OmniGraffle JXA from CSV rep of
class meeting times and column division

Input records look like
B,m,1530,1650,21823,CIS,507
meaning column B of Monday, CIS 507
(course number 21823) is held from 15:30 to
16:50.
Output is a stream of JavaScript commands to
draw the courses in an OmniGraffle document.
"""

import csv
from typing import Tuple, List

# Dimensions
#  (might move to configuration file)
# (in points)
PAGE_HEIGHT_IN = 11
PAGE_WIDTH_IN = 8.5
# Grid in points, with 0.5in margin all sides
PTS = 72
VIEWPORT_HT = (PAGE_HEIGHT_IN - 1) * PTS
VIEWPORT_WD = (PAGE_WIDTH_IN - 1) * PTS
ORIGIN_X = 0.5 * PTS
ORIGIN_Y = 0.5 * PTS
# 6 columns, each divided into 3 subcolumns
COL_WD = VIEWPORT_WD / 6
SUBCOL_WD = COL_WD / 3
# Scale times based on earliest, latest
EARLIEST = 8
LATEST = 18
ROW_HT = VIEWPORT_HT / (LATEST - EARLIEST)


def load(path: str) -> list:
    """Path should refer to CSV file with
    format
    B,m,1530,1650,21823,CIS,507
    Columns: sub-column (A-D), day of week (mtwrf),
    from-time, to-time, CRN, subject code, course
    number.
    """
    schedule = [ ]
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            schedule.append(row)
    return schedule

# Decoding columns, subcolumns, etc
SUBCOL = { "A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
DAYCOL = {"m": 1, "t": 2, "w": 3, "r": 4, "f": 5}

class Meeting:
    """Class meeting, e.g., CIS 607 from 12:00-13:20
    on Tuesday.  Also knows which sub-column the
    meeting should be drawn in (0,1,2,3,4).
    """
    def __init__(self, row: list):
        """row format is
        ['B', 't', '1200', '1320', '21831', 'CIS', '533']
        """
        self.row = row # Useful for debugging?
        col, day, start, end, crn, subj, num = row
        self.day = day
        self.col = col
        self.subcol = SUBCOL[col]
        self.daycol = DAYCOL[day]
        # Start and end hour as floats, e.g., 8.5 = 8:30
        self.start = int(start[0:2]) + int(start[2:4])/60
        self.end = int(end[0:2]) + int(end[2:4])/60
        self.course = subj + " " + num

    def __str__(self):
        return (f"{self.course} {self.start}-{self.end} "
                + f"{self.day} ({self.daycol}) "
                + f"{self.col} ({self.subcol})")
    def rect(self) -> tuple:
        """Returns (ulx, uly, lrx, lry)"""
        height = (self.end - self.start) * ROW_HT
        top = (self.start - EARLIEST) * ROW_HT
        bottom = top + height
        left = self.daycol * COL_WD + self.subcol * SUBCOL_WD
        right = left + SUBCOL_WD
        return (top, left, bottom, right)

    def jax(self):
        top, left, bottom, right = self.rect()
        height = bottom - top
        width = right - left
        return f"""
        var g1 = canvas.newShape();
        g1.strokeColor = Color.RGB(0.5, 0.0, 0.0);
        g1.strokeThickness = 1;
        g1.fillColor = Color.RGB(0.9, 0.9, 0.9);
        g1.geometry = new Rect({left}, {top}, {width}, {height});
        g1.textWraps = false;
        g1.textRotationIsRelative = true;
        g1.textRotation = 90;
        g1.text = "{self.course}"; 
        """
def jax_prolog():
    """Place this once at the top of the
    JavaScript document.
    """
    return f"""
    var canvas = document.windows[0].selection.canvas;
    """

def jax_time_labels():
    """8:00, 9:00 etc down the left side.
    Generating labels here maintains
    consistency with position of meeting boxes.
    """
    labels = [ ]
    for cur in range(int(EARLIEST), int(LATEST)):
        left = 0
        top = (cur - EARLIEST) * ROW_HT
        height = 50 # could this be smaller?
        width = COL_WD * 0.9
        label = f"""
        var g1 = canvas.newShape();
        g1.strokeThickness = 0;
        g1.fillColor = null;
        g1.shadowColor = null; 
        g1.geometry = new Rect({left}, {top}, {width}, {height});
        g1.textVerticalPlacement = VerticalTextPlacement.Top;
        g1.textHorizontalAlignment = HorizontalTextAlignment.Left;
        g1.text = "{cur}:00";  
        """
        labels.append(label)
    return "\n".join(labels)

def jax_hour_rules():
    rules = []
    for cur in range(int(EARLIEST), int(LATEST)):
        left = COL_WD
        top = (cur - EARLIEST) * ROW_HT
        height = 50 # could this be smaller?
        width = COL_WD * 0.9
        rule = f"""
        var g1 = canvas.newLine();
        g1.points = [new Point({left}, {top}), new Point({VIEWPORT_WD}, {top})];
        g1.strokeThickness = 1;
        g1.lineType = LineType.Straight;
        g1.tail = null;
        g1.strokeColor = Color.RGB(0.5, 0.5, 0.5);
        g1.strokeType = StrokeType.Single;
        g1.head = null;
        g1.headType = "";
        g1.strokePattern = StrokeDash.Solid;
        g1.tailMagnet = 0;
        g1.tailType = "";
        """
        rules.append(rule)
    return "\n".join(rules)

def jax_day_columns():
    columns = [ ]
    days = [("Mon", 1), ("Tue", 2),
            ("Wed", 3), ("Thu", 4),
            ("Fri", 5)]
    for name, col in days:
        top = 0
        left = col * COL_WD
        bottom = VIEWPORT_HT
        rule = f"""
        var g1 = canvas.newLine();
        g1.points = [new Point({left}, {top}), new Point({left}, {bottom})];
        g1.strokeThickness = 1;
        g1.lineType = LineType.Straight;
        g1.tail = null;
        g1.strokeColor = Color.RGB(0.5, 0.5, 0.5);
        g1.strokeType = StrokeType.Single;
        g1.head = null;
        g1.headType = "";
        g1.strokePattern = StrokeDash.Solid;
        g1.tailMagnet = 0;
        g1.tailType = "";
        """
        columns.append(rule)
        label = f"""
        var g1 = canvas.newShape();
        g1.strokeThickness = 0;
        g1.fillColor = null;
        g1.geometry = new Rect({left}, {top}, {COL_WD}, {0.5*ROW_HT});
        g1.textVerticalPlacement = VerticalTextPlacement.Top;
        g1.textHorizontalAlignment = HorizontalTextAlignment.Center;
        g1.text = "{name}";          
        """
        columns.append(label)
    return "\n".join(columns)

if __name__ == "__main__":
    schedule = load("../data/2020W.tbl")
    # for row in schedule:
    #     print(row)
    # print("---------")
    # for row in schedule:
    #     mtg = Meeting(row)
    #     print(mtg)
    print(jax_prolog())
    print(jax_time_labels())
    print(jax_hour_rules())
    print(jax_day_columns())
    for row in schedule:
      print(Meeting(row).jax())




