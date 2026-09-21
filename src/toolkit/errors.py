class toolkitError(Exception):
    """for all toolkit errors"""


class calcError(toolkitError):
    """expression cannot be tokenized or calculated"""


class convError(toolkitError):
    """unit conversion is invalid"""