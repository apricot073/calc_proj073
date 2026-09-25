from toolkit.errors import ConvError

units = (
    {
        'm': 1,
        'mm': 10**3,
        'cm': 10**2,
        'km': 10**-3
    },

    {
        'kg': 1,
        'g': 10**3
    },

    {
        'c': [1, 0],
        'f': [9/5, 32],
        'k': [1, 273.15]
    }
)


def Convert(value, from_unit, to_unit):
    group_from = None
    group_to = None
    found = False
    from_unit = str.lower(from_unit)
    to_unit = str.lower(to_unit)
    for sublist in units:
        if from_unit in sublist:
            group_from = sublist
        if to_unit in sublist:
            group_to = sublist
        if group_to is group_from is not None:
            found = True
            if type(sublist[from_unit]) is not list:
                in_standard = value / sublist[from_unit]
                answer = in_standard * sublist[to_unit]
            else:
                in_standard = (value - sublist[from_unit][1]) / sublist[from_unit][0]
                if in_standard < -273.15:
                    raise ConvError('Invalid temperature.')
                answer = in_standard * sublist[to_unit][0] + sublist[to_unit][1]

            return float(answer)
    if not found:
        if group_to is None or group_from is None:
            raise ConvError('Unknown unit.')
        else:
            raise ConvError('Incompatible units.')
