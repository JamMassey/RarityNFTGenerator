import decimal

def format_number(num):
    try:
        dec = decimal.Decimal(num)
    except:
        raise RuntimeError
    tup = dec.as_tuple()
    delta = len(tup.digits) + tup.exponent
    digits = ''.join(str(d) for d in tup.digits)
    if delta <= 0:
        zeros = abs(tup.exponent) - len(tup.digits)
        val = '0.' + ('0'*zeros) + digits
    else:
        val = digits[:delta] + ('0'*tup.exponent) + '.' + digits[delta:]
    val = val.rstrip('0')
    if val[-1] == '.':
        val = val[:-1]
    if tup.sign:
        return '-' + val
    return val

#Needs vectorising
def overlay(base, overlay):
    for j in range(base.size[1]):
        for i in range(base.size[0]):
            if overlay.getpixel((i, j)) != (0,0,0,0):
                base.putpixel((i,j), overlay.getpixel((i, j)))
    return base
