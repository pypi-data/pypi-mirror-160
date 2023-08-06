# Web converter

This is a simple package that converts headers and cookies
You can pass a string containing headers and cookies to it, and it will return you a dictionary understandable for the requests module.

### Usage:
```
>>> from web_converter.converter import convert
>>> string = 'Referer: https://github.com/'
>>> example = convert(string)
>>> print(example)
{'Referer': 'https://github.com/'}
>>> print(type(example))
<class 'dict'>