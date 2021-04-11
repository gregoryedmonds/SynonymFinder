import math

def cosine_singularity(v1, v2):
    sumxx, sumyy, sumxy = 0,0,0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    endValue = sumxy/math.sqrt(sumxx*sumyy)
    return endValue