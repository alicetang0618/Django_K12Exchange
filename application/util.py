from models import *

def avgrating(material):
    ratings = Rating.objects.filter(material = material)
    num = 0
    totalrating = 0
    for rate in ratings:
        totalrating += rate.rate
        num += 1
    if num == 0:
        avgrating = 0
    else: 
        avgrating = int(totalrating/num)
    return avgrating


def order_by_popularity(materials):
    rv = []
    for material in materials:
        rv.append((len(Download.objects.filter(material=material)), material))
    rv = sorted(rv, reverse=True)
    rv = [y for (x,y) in rv]
    return rv


def order_by_rating(materials):
    rv = []
    for material in materials:
        rv.append((avgrating(material), material))
    rv = sorted(rv, reverse=True)
    rv = [y for (x,y) in rv]
    return rv