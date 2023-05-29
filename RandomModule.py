from random import *
import QuestionModule as qm
import fractions as fr
import math as mt

"""
Each function takes in a difficulty value and randomly generate the key values for QuestionModule function and return the corresponding function's return value
All function in this module has to be registered in the funcpicker with a unique index number
And all index number has to be registered in databases/setlist.json to be able to work
"""


def gnThreeops(dif):
    typ = choice(["+", "-", "*"])
    a = randint(0, int(10 ** dif))
    b = randint(0, int(10 ** dif))
    if typ == "*":
        if a // 10 > 0 and b // 10 > 0:
            a //= 10
            b //= 10

    return qm.threeOps(a, b, typ)


def gnDivision(dif):
    if dif <= 1:
        typ = "integer"
    elif dif <= 2:
        typ = choices(["integer", "remainder"], [1, dif - 1])[0]
    else:
        typ = choices(["integer", "remainder", "decimal"], [1, 1, dif - 2])[0]

    if typ == "integer":
        b = randint(1, int(4 ** dif) + 1)
        mult = randint(1, int(4 ** dif) + 1)
        a = b * mult
        dp = 0
    elif typ == "remainder":
        b = randint(1, int(4 ** dif) + 1)
        a = randint(b, int(4 ** dif) + 1)
        dp = -1
    elif typ == "decimal":
        b = randint(1, int(4 ** dif) + 1)
        a = randint(b, int(4 ** dif) + 1)
        dp = randint(0, int(dif))

    return qm.division(a, b, dp)


def gnFractionOfAmount(dif):
    if dif <= 2:
        typ = "integer"
    else:
        typ = choices(["integer", "decimal"], [2, dif - 2])[0]

    if typ == "integer":
        den = randint(2, int(4 ** dif) * 2)
        num = randint(1, den - 1)
        num, den = fr.Fraction(num, den).numerator, fr.Fraction(num, den).denominator
        amount = den * randint(1, int(4 ** dif))
        dp = 0
    elif typ == "decimal":
        den = randint(2, int(4 ** dif) * 2)
        num = randint(1, den - 1)
        num, den = fr.Fraction(num, den).numerator, fr.Fraction(num, den).denominator
        dp = choice([-1, randint(0, int(dif))])
        amount = randint(1, int(8 ** dif))

    return qm.fractionOfAmount(num, den, amount, dp)


def gnFractionalChange(dif):
    if dif <= 2:
        typ = "integer"
    else:
        typ = choices(["integer", "decimal"], [2, dif - 2])[0]

    change = choice(["+", "-"])
    if typ == "integer":
        den = randint(2, int(4 ** dif) * 2)
        num = randint(1, den - 1)
        num, den = fr.Fraction(num, den).numerator, fr.Fraction(num, den).denominator
        amount = den * randint(1, int(4 ** dif))
        dp = 0
    elif typ == "decimal":
        den = randint(2, int(4 ** dif) * 2)
        num = randint(1, den - 1)
        num, den = fr.Fraction(num, den).numerator, fr.Fraction(num, den).denominator
        dp = choice([-1, randint(0, int(dif))])
        amount = randint(1, int(8 ** dif))

    return qm.fractionalChange(num, den, amount, change, dp)


def gnPercentageOfAmount(dif):
    percentage = randint(1, 99)
    amount = randint(1, int(10 ** dif))

    return qm.percentageOfAmount(percentage, amount)


def gnPercentageChange(dif):
    oldAmount = randint(1, int(10 ** dif))
    newAmount = randint(1, int(10 ** dif))

    return qm.percentageChange(oldAmount, newAmount)


def gnRepeatedPercentageChange(dif):
    originalAmount = randint(1, int(10 ** dif))
    percentage = randint(1, mt.ceil(dif) * 100)
    change = choice(["+", "-"])
    iterations = randint(2, (mt.ceil(dif * 5) + 1) * 2)
    dp = randint(0, int(dif))

    return qm.repeatedPercentageChange(originalAmount, percentage, iterations, change, dp)


def gnRatio(dif):
    typ = choice(["share", "reverse", "difference"])
    ratio = [randint(1, 3 * mt.ceil(dif)) for i in range(int(dif + 2))]
    unit = randint(1, 3 * int(dif))

    return qm.ratio(unit, ratio, typ)


def gnFactors(dif):
    number = randint(1, int(6 ** dif))

    return qm.factors(number)


def gnhcf(dif):
    a = randint(1, int(6 ** dif))
    b = randint(1, int(6 ** dif))

    return qm.hcf(a, b)


def gnlcm(dif):
    a = randint(1, int(6 ** dif))
    b = randint(1, int(6 ** dif))

    return qm.lcm(a, b)


def gnSimplifyingFractions(dif):
    num = randint(1, int(6 ** dif))
    den = randint(1, int(6 ** dif))

    return qm.simplifyingFractions(num, den)


def gnArithmeticSequence(dif):
    if dif <= 2:
        a = randint(0, int(10 ** dif))
        k = randint(0, int(5 ** dif))
    else:
        a = randint(-int(5 ** dif), int(10 ** dif))
        k = randint(-int(3 ** dif), int(5 ** dif))
    n = randint(0, 10 * mt.ceil(dif))

    return qm.arithmeticSequence(a, k, n)


def gnFourOpsFractions(dif):
    typ = choice(["+", "-", "*", "/"])
    d1 = randint(2, int(4 ** dif))
    n1 = randint(1, d1 - 1)
    n1, d1 = fr.Fraction(n1, d1).numerator, fr.Fraction(n1, d1).denominator
    d2 = randint(2, int(4 ** dif))
    n2 = randint(1, d2 - 1)
    n2, d2 = fr.Fraction(n2, d2).numerator, fr.Fraction(n2, d2).denominator

    return qm.fourOpsFractions(n1, d1, n2, d2, typ)


def gnmmmr(dif):
    target = choice(["mean", "median", "mode", "range"])
    serie = [randint(1, int(3 ** dif)) for i in range(randint(mt.ceil(dif) * 3 + 1, mt.ceil(dif) * 5 + 1))]
    dp = randint(0, int(dif))

    return qm.mmmr(serie, target, dp)


def gnToStandardForm(dif):
    a = round(random(), mt.ceil(dif)) * (10 ** randint(1, mt.ceil(dif) * 3))

    return qm.toStandardForm(a)


def gnFromStandardForm(dif):
    a = round(random(), mt.ceil(dif))
    e = randint(1, mt.ceil(dif) * 3)

    return qm.fromStandardForm(a, e)


def gnSpeedDistTime(dif):
    speed_unit_list = {"m/s": 1, "m/min": 60, "m/h": 3600, "km/s": 0.001, "km/min": 0.06, "km/h": 3.6, }
    time_unit_list = {"s": 1, "min": fr.Fraction(1, 60), "h": fr.Fraction(3600)}
    dist_unit_list = {"m": 1, "km": 0.001}
    if dif < 1:
        speedu = "m/s"
        timeu = "s"
        distu = "m"
        speed = randint(1, int(5 ** dif) * 2)
        time = randint(1, int(5 ** dif) * 2)
        dist = speed * time
    elif dif < 3:
        speedu = choice(list(speed_unit_list))
        distu, timeu = speedu.split("/")
        speed = randint(1, int(5 ** dif) * 2)
        time = randint(1, int(5 ** dif) * 2)
        dist = speed * time
    else:
        speed = randint(1, int(5 ** dif) * 2)
        time = randint(1, int(5 ** dif) * 2)
        dist = speed * time
        speedu = choice(list(speed_unit_list))
        timeu = choice(list(time_unit_list))
        distu = choice(list(dist_unit_list))
        speed *= speed_unit_list[speedu]
        time *= time_unit_list[timeu]
        dist *= dist_unit_list[distu]
    target = choice(["dist", "speed", "time"])

    return qm.speedDistTime(speed, speedu, time, timeu, dist, distu, target)


def gnDiscreteDistribution(dif):
    target = choice(["mean", "variance"])
    table = {}
    s = 1
    leng = randint(1, mt.ceil(dif) * 3)
    r_list = [randint(1, int(3 ** dif)) for i in range(leng)]
    for i in range(leng):
        table[i + 1] = fr.Fraction(r_list[i], sum(r_list))
    dp = randint(0, int(dif))

    return qm.discreteDistribution(table, target, dp)


# A dictionary that maps index numbers with functions
funcPicker = {
    1: gnThreeops,
    2: gnDivision,
    3: gnFractionOfAmount,
    4: gnFractionalChange,
    5: gnPercentageOfAmount,
    6: gnPercentageChange,
    7: gnRepeatedPercentageChange,
    8: gnRatio,
    9: gnSpeedDistTime,
    11: gnFactors,
    12: gnhcf,
    13: gnlcm,
    14: gnSimplifyingFractions,
    15: gnArithmeticSequence,
    16: gnFourOpsFractions,
    17: gnmmmr,
    18: gnToStandardForm,
    19: gnFromStandardForm,
    20: gnDiscreteDistribution
}
