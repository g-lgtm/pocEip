#! /usr/bin/env python3

TARGET_COLORS = {"Red": (255, 0, 0), "Yellow": (254, 254, 0), "Green": (0, 254, 0), "White": (255, 255, 255), "Black": (0, 0, 0)}

def color_difference(color1, color2):
    return sum([abs(component1-component2) for component1, component2 in zip(color1, color2)])

def getColor(rgbColor : tuple):
    my_color = rgbColor
    differences = [[color_difference(my_color, target_value), target_name] for target_name, target_value in TARGET_COLORS.items()]
    differences.sort()
    return (differences[0][1])