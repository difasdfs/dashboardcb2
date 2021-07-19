import math

def main(orderan, orderan_awal):
    maksimal = lambda x: math.ceil(x) + math.ceil(x*0.1)
    minimal = lambda x: math.ceil(x) - math.ceil(x*0.1)

    min = minimal(orderan_awal)
    max = maksimal(orderan_awal)

    if orderan <= min:
        hasil = min
    elif orderan >= max:
        hasil = max
    else:
        hasil = orderan

    return hasil