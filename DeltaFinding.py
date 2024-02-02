def delta_finding(lower_corner, upper_corner):
    return '{},{}'.format(
        str(abs(float(lower_corner[0]) - float(upper_corner[0]))),
        str(abs(float(lower_corner[1]) - float(upper_corner[1])))
    )
