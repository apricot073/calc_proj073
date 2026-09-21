class toolkitError(Exception):
    """for all toolkit errors"""


class calculatorError(toolkitError):
    """expression cannot be tokenized or calculated"""


class converterError(toolkitError):
    """unit conversion is invalid"""