import math as mt
import fractions as fr
import statistics as st
from random import *

"""
Each function takes in a few key values and generate corresponding questions and answeres
Question part consists of a list, where each line is a string to be displayed in an independant line
Answer part consists of a dictionary, where each key is the name for the required answer and value is the answered
The key of an answer dictionary can be splitted by a "|" which the later part will be displayed after the input box
If a section in question string is to be displayed in LaTeX formula, it has to be closed in \(content\) for inline or \[content\] for independant login_error
All answers are to be compared in string form and must be stored in one of the fundamental datatypes
A function in this module needs to have a corresponding function in RandomModule to be able to work
"""


def ordinal(x):
    if x > 10 and x < 20:
        return str(x) + "th"
    elif x % 10 == 1:
        return str(x) + "st"
    elif x % 10 == 2:
        return str(x) + "nd"
    elif x % 10 == 3:
        return str(x) + "rd"
    else:
        return str(x) + "th"


def idf(x, dp):
    if x == int(x):
        question = ""
        answer = int(x)
    elif dp < 0:
        question = r"as a simplest fraction"
        answer = str(fr.Fraction(str(x)).limit_denominator(100000))
    elif dp > 0:
        question = " to {} d.p.".format(dp)
        answer = float(round(x, dp))
    else:
        question = " to nearest integer"
        answer = int(round(x, 0))
    return question, answer


def rounding(x, dp):
    question = [r"Round \({}\) to {} d.p.".format(str(x), str(dp))]
    answer = {"Answer": round(x, dp)}

    return {"question": question, "answer": answer}


def sigFigs(x, sf):
    digits = mt.floor(mt.log10(x)) + 1
    question = [r"Round {} to {}s.f.".format(x, dp)]
    answer = {"Answer": round(x, sf - digits)}
    return {"question": question, "answer": answer}


def threeOps(x, y, typ):

    if typ == "+":
        question = [r"\[{}+{}\]".format(x, y)]
        answer = {"Answer": x + y}
    elif typ == "-":
        question = [r"\[{}-{}\]".format(x, y)]
        answer = {"Answer": x - y}
    elif typ == "*":
        question = [r"\[{}\times{}\]".format(x, y)]
        answer = {"Answer": x * y}

    return {"question": question, "answer": answer}


def division(x, y, dp):
    question = [r"\[{}\div{}\]".format(x, y)]
    if x == int(x / y):
        answer = {"Answer": int(x / y)}
    elif dp < 0:
        question[0] += r" in integer quotient and remainder"
        answer = {"Quotient": x // y, "Remainder": x % y}
    elif dp > 0:
        question[0] += r" to {} d.p.".format(dp)
        answer = {"Answer": round(x / y, dp)}
    else:
        question[0] += r" to nearest integer"
        answer = {"Answer": int(round(x / y, 0))}

    return {"question": question, "answer": answer}


def fractionOfAmount(num, den, amount, dp):
    answer = {}
    question = [r"\(\frac{{{}}}{{{}}}\) of \({}\)".format(num, den, amount)]
    ques, answer["Answer"] = idf(num / den * amount, dp)
    question[0] += ques

    return {"question": question, "answer": answer}


def fractionalChange(num, den, amount, change, dp):
    answer = {}
    if change == "+":
        question = [r"\({}\) increased by\(\frac{{{}}}{{{}}}\)".format(amount, num, den)]
        ques, answer["Answer"] = idf(amount + amount * num / den, dp)
    elif change == "-":
        question = [r"\({}\) decreased by\(\frac{{{}}}{{{}}}\)".format(amount, num, den)]
        ques, answer["Answer"] = idf(amount - amount * num / den, dp)
    question[0] += ques

    return {"question": question, "answer": answer}


def percentageOfAmount(percentage, amount):
    question = [r"\({}\%\) of \({}\) in percentage".format(percentage, amount)]
    answer = {"Answer": percentage / 100 * amount}

    return {"question": question, "answer": answer}


def percentageChange(oldAmount, newAmount):
    question = [r"The change from \({}\) to \({}\) in percentage".format(oldAmount, newAmount)]
    answer = {"Answer|%": round((newAmount - oldAmount) / oldAmount * 100, 0)}

    return {"question": question, "answer": answer}


def repeatedPercentageChange(originalAmount, percentage, iterations, change, dp):
    answer = {}
    if change == "+":
        question = [r"\({}\) increased by \({}\%\) after \({}\) repetitions".format(originalAmount, percentage, iterations)]
        ques, answer["Answer"] = idf(originalAmount * ((1 + percentage / 100) ** iterations), dp)
    elif change == "-":
        question = [r"\({}\) increased by \({}\%\) after \({}\) repetitions".format(originalAmount, percentage, iterations)]
        ques, answer["Answer"] = idf(originalAmount * ((1 - percentage / 100) ** iterations), dp)
    question[0] += ques

    return {"question": question, "answer": answer}


def ratio(unit, ratio, typ):
    if typ == "share":
        anslis = [(i * unit) for i in ratio]
        question = [r"Share \({}\) in the ratio \({}\)".format(unit * sum(ratio), ":".join(map(str, ratio)))]
        answer = {}
        for i in range(len(anslis)):
            answer[str(i + 1)] = anslis[i]
    elif typ == "reverse":
        ind = randint(1, len(ratio)) - 1
        question = [r"In an amount divide into the ratio \({}\), the {} term equals to \({}\), find the amount".format(":".join(map(str, ratio)), ordinal(ind + 1), ratio[ind] * unit)]
        answer = {"Answer": unit * sum(ratio)}
    elif typ == "difference":
        indA, indB = sample(range(len(ratio)), 2)
        question = [r"An amount is shared in the ratio \({}\), the {} term is ".format(":".join(map(str, ratio)), ordinal(indA + 1))]
        if ratio[indA] > ratio[indB]:
            question[0] += str(unit * ratio[indA] - unit * ratio[indB]) + r" more than the"
            answer = {"Answer": unit * sum(ratio)}
        else:
            question[0] += str(unit * ratio[indB] - unit * ratio[indA]) + r" less than the "
            answer = {"Answer": unit * sum(ratio)}
        question[0] += r"{} term, find the amount".format(ordinal(indB + 1))

    return {"question": question, "answer": answer}


def factors(number):
    question = [r"List all factors of \({}\) in acsending order".format(number)]
    anslis = []
    for i in range(1, number + 1):
        if number % i == 0:
            anslis.append(i)
    answer = {}
    for i in range(len(anslis)):
        answer[str(i + 1)] = anslis[i]

    return {"question": question, "answer": answer}


def hcf(x, y):
    question = [r"The highest common factor of \({}\) and \({}\)".format(x, y)]
    while x != y:
        if x < y:
            y = y - x
        else:
            x = x - y
    answer = {"Answer": x}
    return {"question": question, "answer": answer}


def lcm(x, y):
    question = [r"The lowest common multiple of \({}\) and \({}\)".format(x, y)]
    z = x
    while z % y > 0:
        z += x
    answer = {"Answer": z}
    return {"question": question, "answer": answer}


def simplifyingFractions(num, den):
    question = [r"Simplify \(\frac{{{}}}{{{}}}\)".format(num, den)]
    answer = {"Answer": str(fr.Fraction(num, den))}

    return {"question": question, "answer": answer}


def arithmeticSequence(a, k, n):
    list = [(a + k * i) for i in range(3)]
    question = [r"In an arithmetic sequence starting with \({}\), find the {} term".format("\,".join(map(str, list)), ordinal(n))]
    answer = {"Answer": a + k * (n - 1)}

    return {"question": question, "answer": answer}


def speedDistTime(speed, speedu, time, timeu, dist, distu, target):
    if target == "dist":
        question = [r"The speed is \({}{}\), the time used is \({}{}\), find the distance traveled in \({}\)".format(speed, speedu, time, timeu, distu)]
        answer = {"Answer|{}".format(distu): str(dist)}
    elif target == "speed":
        question = [r"The distance travelled is \({}{}\), the time used is \({}{}\), find the speed in \({}\)".format(dist, distu, time, timeu, speedu)]
        answer = {"Answer|{}".format(speedu): str(speed)}
    elif target == "time":
        question = [r"The speed is \({}{}\), the distance travelled \({}{}\), find time used in \({}\)".format(speed, speedu, dist, distu, timeu)]
        answer = {"Answer|{}".format(timeu): str(time)}

    return {"question": question, "answer": answer}


def fourOpsFractions(n1, d1, n2, d2, typ):
    if typ == "+":
        question = [r"\(\frac{{{}}}{{{}}}+\frac{{{}}}{{{}}}\) in simplest form".format(n1, d1, n2, d2)]
        answer = {"Answer": str(fr.Fraction(n1, d1) + fr.Fraction(n2, d2))}
    elif typ == "-":
        question = [r"\(\frac{{{}}}{{{}}}-\frac{{{}}}{{{}}}\) in simplest form".format(n1, d1, n2, d2)]
        answer = {"Answer": str(fr.Fraction(n1, d1) - fr.Fraction(n2, d2))}
    elif typ == "*":
        question = [r"\(\frac{{{}}}{{{}}}\times\frac{{{}}}{{{}}}\) in simplest form".format(n1, d1, n2, d2)]
        answer = {"Answer": str(fr.Fraction(n1, d1) * fr.Fraction(n2, d2))}
    elif typ == "/":
        question = [r"\(\frac{{{}}}{{{}}}\div\frac{{{}}}{{{}}}\) in simplest form".format(n1, d1, n2, d2)]
        answer = {"Answer": str(fr.Fraction(n1, d1) / fr.Fraction(n2, d2))}

    return {"question": question, "answer": answer}


def mmmr(serie, target, dp):
    answer = {}
    if target == "mean":
        question = [r"Find the mean of these values"]
        ques, answer["Answer"] = idf(st.mean(serie), dp)
    elif target == "median":
        question = [r"Find the median of these values"]
        ques, answer["Answer"] = idf(st.median(serie), dp)
    elif target == "mode":
        question = [r"Find the mode of these values"]
        try:
            ques, answer["Answer"] = idf(st.mode(serie), dp)
        except:
            question = [r"Find the mean of these values"]
            ques, answer["Answer"] = idf(st.mean(serie), dp)
    elif target == "range":
        question = [r"Find the range of these values:"]
        answer = {"Answer": max(serie) - min(serie)}
        ques = ""
    question[0] += ques
    question.append(r"\[{}\]".format("\:".join(map(str, serie))))

    return {"question": question, "answer": answer}


def toStandardForm(x):
    question = [r"Write \({}\) in scientific standard form xey where x is a constant. and y is an integer".format(x)]
    digits = mt.floor(mt.log10(x))
    x /= (10 ** digits)
    answer = {"Answer": str() + "e" + str(digits)}

    return {"question": question, "answer": answer}


def fromStandardForm(x, e):
    question = [r"Write \({}\times10^{}\) in ordinary number".format(x, e)]
    answer = {"Answer": round(x, 6) * (10 ** e)}

    return {"question": question, "answer": answer}


def discreteDistribution(table, target, dp):
    answer = {}
    question = ["In the following random distribution"]
    prob_list = [r"\[\frac{{{}}}{{{}}}\]".format(i.numerator, i.denominator) for i in table.values()]
    question.append(r"<table><tr>{}</tr><tr>{}</tr></table>".format("".join(r"<th>{}</th>".format(key) for key in table.keys()), "".join(r"<td>{}</td>".format(prob) for prob in prob_list)))
    if target == "mean":
        question.append("Find the expected value")
        mean = 0
        for key, value in table.items():
            mean += key * value
        ques, answer["Answer"] = idf(mean, dp)
        question[2] += ques
    elif target == "variance":
        question.append("Find the variance")
        mean = 0
        vari = 0
        for key, value in table.items():
            mean += key * value
        for key, value in table.items():
            vari += (key - mean) ** 2 * value
        ques, answer["Answer"] = idf(vari, dp)
        question[2] += ques

    return {"question": question, "answer": answer}
