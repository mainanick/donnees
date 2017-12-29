# Copyright (c) 2017 Maina Nick

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE


class Attrvalue(dict):
    """Allow Getting value of dict from attribute

    Example:
      JOIN = Attrvalue({'INNER':"INNER JOIN", 'OUTER':"OUTER JOIN"})
      print(JOIN.INNER) # prints INNER JOIN
    """

    def __getattribute__(self, attr):
        return super().__getitem__(attr)


def format(formatter, payload):
    """Returns a list of formatted strings
    Example:
    >>> formatter = "{} is {}"
    >>> data = {"name":"donnees", "age":1}
    >>> result = format(formatter, data)
    >>> print(result[0])
    name is donnees
    >>> print(result[1])
    age is 1

    Or

    >>> formatter = lamdba x: "{} haha".format(x)
    >>> data = ["name", "age"]
    >>> result = format(formatter, data)
    >>> print(result[0])
    name haha
    >>> print(result[1])
    age haha
    """
    if not isinstance(payload, (list, tuple, dict)):
        raise ValueError("Unexpected Payload {}".format(payload))

    if isinstance(payload, (list, tuple)):
        if callable(formatter):
            return [formatter(k) for k in payload]
        return [formatter.format(k) for k in payload]
    # At this point the payload is dict
    return [formatter.format(k, v) for k, v in payload.items()]
