#!/opt/bin/lv_micropython -i

import lvgl as lv
import display_driver

display_driver.getdisplay_landscape()


def LV_GRID_FR(x):
    return lv.COORD.MAX - 100 + x
#
# Demonstrate grid's "free unit"
#

# Column 1: fix width 60 px
# Column 2: 1 unit from the remaining free space
# Column 3: 2 unit from the remaining free space

col_dsc = [60, LV_GRID_FR(1), LV_GRID_FR(2), lv.COORD.MAX]

# Row 1: fix width 60 px
# Row 2: 1 unit from the remaining free space
# Row 3: fix width 60 px

row_dsc = [40, LV_GRID_FR(1), 40, lv.COORD.MAX]

# Create a container with grid
cont = lv.obj(lv.scr_act())
cont.set_size(300, 220)
cont.center()
cont.set_grid_dsc_array(col_dsc, row_dsc)

for i in range(9):
    col = i % 3
    row = i // 3

    obj = lv.obj(cont)
    # Stretch the cell horizontally and vertically too
    # Set span to 1 to make the cell 1 column/row sized
    obj.set_grid_cell(lv.GRID_ALIGN.STRETCH, col, 1,
                      lv.GRID_ALIGN.STRETCH, row, 1)

    label = lv.label(obj)
    label.set_text("%d,%d"%(col, row))
    label.center()

