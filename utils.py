from decimal import *

def time_to_str(time):
    if time < Decimal("0.000000001"):
        return str(time.scaleb(12)) + "ps"
    elif time < Decimal("0.000001"):
        return str(time.scaleb(9)) + "ns"
    elif time < Decimal("0.001"):
        return str(time.scaleb(6)) + "us"
    elif time < 1:
        return str(time.scaleb(3)) + "ms"
    else:
        return str(time) + "s"

def parse_time(time_str):
    if time_str.lower().endswith("fs"):
        return Decimal(time_str[:-2]).scaleb(-15)
    if time_str.lower().endswith("f"):
        return Decimal(time_str[:-1]).scaleb(-15)
    elif time_str.lower().endswith("ps"):
        return Decimal(time_str[:-2]).scaleb(-12)
    elif time_str.lower().endswith("p"):
        return Decimal(time_str[:-1]).scaleb(-12)
    elif time_str.lower().endswith("ns"):
        return Decimal(time_str[:-2]).scaleb(-9)
    elif time_str.lower().endswith("n"):
        return Decimal(time_str[:-1]).scaleb(-9)
    elif time_str.lower().endswith("us"):
        return Decimal(time_str[:-2]).scaleb(-6)
    elif time_str.lower().endswith("u"):
        return Decimal(time_str[:-1]).scaleb(-6)
    elif time_str.lower().endswith("µs"):
        return Decimal(time_str[:-2]).scaleb(-6)
    elif time_str.lower().endswith("µ"):
        return Decimal(time_str[:-1]).scaleb(-6)
    elif time_str.lower().endswith("ms"):
        return Decimal(time_str[:-2]).scaleb(-3)
    elif time_str.lower().endswith("m"):
        return Decimal(time_str[:-1]).scaleb(-3)
    elif time_str.lower().endswith("ks"):
        return Decimal(time_str[:-2]).scaleb(3)
    elif time_str.lower().endswith("k"):
        return Decimal(time_str[:-1]).scaleb(3)
    elif time_str.lower().endswith("megs"):
        return Decimal(time_str[:-4]).scaleb(6)
    elif time_str.lower().endswith("meg"):
        return Decimal(time_str[:-3]).scaleb(6)
    elif time_str.lower().endswith("gs"):
        return Decimal(time_str[:-2]).scaleb(9)
    elif time_str.lower().endswith("g"):
        return Decimal(time_str[:-1]).scaleb(9)
    elif time_str.lower().endswith("ts"):
        return Decimal(time_str[:-2]).scaleb(12)
    elif time_str.lower().endswith("t"):
        return Decimal(time_str[:-1]).scaleb(12)
    else:
        return Decimal(time_str)
