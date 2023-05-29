from tinydb import *
from math import *

# Estimate difficulty from ability


def estimate_dif(matrix):
    max_probability = -1
    max_difficulty = -1
    for difficulty10 in range(-100, 501):
        difficulty = difficulty10 / 10  # Loop the possible difficulty from 0.0 to 10.0, increased by 0.1 each stem
        probability = 1
        for row in matrix:  # Loop through all exam records
            total_questions = len(row["marks"])
            num = exp((row["marks"].count(1)) * (row["ability"] - difficulty))
            den = 0
            for j in range(total_questions + 1):
                den += exp((j + 1) * (row["ability"] - difficulty))
            probability *= num / den  # Multiply the result probability together
        if max_probability < probability:  # Find the maximum probability and the difficulty that works it out
            max_probability = probability
            max_difficulty = difficulty
    return max_difficulty

# Estimate ability from difficulty, quite the inverse of the above function


def estimate_abil(matrix):
    max_probability = -1
    max_ability = -1
    for ability10 in range(-100, 501):
        ability = ability10 / 10
        probability = 1
        for row in matrix:
            total_questions = len(row["marks"])
            num = exp((row["marks"].count(1)) * (ability - row["difficulty"]))
            den = 0
            for j in range(total_questions + 1):
                den += exp((j + 1) * (ability - row["difficulty"]))
            probability *= num / den
        if max_probability < probability:
            max_probability = probability
            max_ability = ability
    return max_ability
