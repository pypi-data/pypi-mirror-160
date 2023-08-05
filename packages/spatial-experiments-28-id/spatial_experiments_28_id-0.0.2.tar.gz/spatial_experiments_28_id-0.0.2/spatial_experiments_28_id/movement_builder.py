def makeVerticalLine(high_y, low_y, lowest_y, high_x, low_x, step_size, num_steps):
    """
    return a list of tuples of the x,y positions for a scan. The positions form
    a vertical line that can be diagonal.
    """
    line_positions = []
    m = (high_x - low_x) / (high_y - low_y)
    b = high_x - m * high_y
    for step in range(num_steps):
        if high_y > low_y:
            y = lowest_y + (step * step_size)
        else:
            y = lowest_y - (step * step_size)
        x = m * y + b
        line_positions.append((x, y))
    return line_positions


def makeHorizontalLine(high_x, low_x, lowest_x, high_y, low_y, step_size, num_steps):
    """
    return a list of tuples of the x,y positions for a scan. The positions form
    a horizontal line that can be diagonal.
    """
    line_positions = []
    m = (high_y - low_y) / (high_x - low_x)
    b = high_y - m * high_x
    for step in range(num_steps):
        if high_x > low_x:
            x = lowest_x + (step * step_size)
        else:
            x = lowest_x - (step * step_size)
        y = m * x + b
        line_positions.append((x, y))
    return line_positions


def makeGrid(vert_high_y, vert_low_y, vert_lowest_y, vert_high_x, vert_low_x,
             vert_step_size, vert_num_steps, horz_high_x, horz_low_x, horz_lowest_x,
             horz_high_y, horz_low_y, horz_step_size, horz_num_steps):
    """
    return a list of tuples of the x,y positions for a scan. The positions form
    a grid that can be skewed.
    """
    grid_positions = []
    vert_m = (vert_high_x - vert_low_x) / (vert_high_y - vert_low_y)
    vert_b = vert_high_x - vert_m * vert_high_y
    horz_m = (horz_high_y - horz_low_y) / (horz_high_x - horz_low_x)
    horz_b = horz_high_y - horz_m * horz_high_x
    for vert_step in range(vert_num_steps):
        if vert_high_y > vert_low_y:
            vert_y = vert_lowest_y + (vert_step * vert_step_size)
        else:
            vert_y = vert_lowest_y - (vert_step * vert_step_size)
        vert_x_center = vert_m * vert_y + vert_b
        for horz_step in range(horz_num_steps):
            if horz_high_x > horz_low_x:
                x = horz_lowest_x + (horz_step * horz_step_size) + (vert_x_center - vert_low_x)
            else:
                x = horz_lowest_x - (horz_step * horz_step_size) + (vert_x_center - vert_low_x)
            y = (horz_m * x + horz_b) + (vert_y - horz_low_y)
            grid_positions.append((x, y))
    return grid_positions
