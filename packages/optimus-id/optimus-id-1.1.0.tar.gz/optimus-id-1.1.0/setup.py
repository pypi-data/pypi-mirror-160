# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optimus_id']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'optimus-id',
    'version': '1.1.0',
    'description': "Transform internal id's to obfuscated integers using Knuth's integer hash",
    'long_description': "[![Build Status](https://travis-ci.com/mpcabd/python-optimus.svg?branch=main)](https://travis-ci.com/mpcabd/python-optimus)\n\n# python-optimus\nThis is based fully on [pjebs/optimus-go](https://github.com/pjebs/optimus-go) for Go which is based on [jenssegers/optimus](https://github.com/jenssegers/optimus) for PHP which is based on Knuth's Integer Hashing (Multiplicative Hashing) from his book [The Art Of Computer Programming, Vol. 3, 2nd Edition](https://archive.org/details/B-001-001-250/page/n535/mode/2up), Section 6.4, Page 516.\n\nWith this library, you can transform your internal id's to obfuscated integers based on Knuth's integer hash. It is similar to [Hashids](https://hashids.org/), but will generate integers instead of random strings. It is also super fast.\n\n    >>> my_optimus.encode(42)\n    7773166408443174426\n    >>> my_optimus.decode(7773166408443174426)\n    42\n\nThis library supports both 32 and 64 bits integers, although in Python you don't have that differentiation between int32 and int64, even bigint or bignum is the same since [PEP 237](https://www.python.org/dev/peps/pep-0237/). The reason you need a bitlength is that the algorithm itself works on a fixed bitlength. By default this library uses 64 bits.\n\n## Python Support\n\nSo far it's only tested on Python 3.8 and Python 3.9\n\n## Installation\n\n    pip install python-optimus\n\n## Usage\n\nBasic usage:\n\n```python\nfrom optimus_ids import Optimus\nmy_optimus = Optimus(\n    prime=<your prime number>\n)\nmy_int_id = <some id you have>\nmy_int_id_hashed = my_optimus.encode(my_int_id)\nassert my_int_id == my_optimus.decode(my_int_id_hashed)\n```\n\nThe caveat with the usage above is that every time you create your `Optimus` instance it will have a random component, even with using the same prime, so a proper usage should be like this:\n\n```python\nfrom optimus_ids import Optimus\nmy_optimus = Optimus(\n    prime=<your prime number>,\n    random=<some random number>\n)\nmy_int_id = <some id you have>\nmy_int_id_hashed = my_optimus.encode(my_int_id)\nassert my_int_id == my_optimus.decode(my_int_id_hashed)\n\n```\n\nTo generate a suitable random number you could do this:\n\n```python\nfrom optimus_ids import rand_n, MAX_64_INT  # use 32 instead of 64 if you want to\nmy_random_number = rand_n(MAX_64_INT - 1)\n```\n\nYou can also generate an `Optimus` intance and then keep its `prime`, `inverse` and `random` properties stored, so you can always configure a new instance with the same components, or even pickle it:\n\n```python\nfrom optimus_ids import generate, Optimus\nmy_optimus = generate()\n\n# store the following variables or pickle the my_optimus variable\nprime = my_optimus.prime\ninverse = my_optimus.inverse\nrandom = my_optimus.random\nbitlength = my_optimus.bitlength\n\n# create a new instance with the same parameters or unpickle an instance\nmy_other_optimus = Optimus(\n    prime=prime,\n    inverse=inverse,\n    random=random,\n    bitlength=bitlength,\n)\nassert my_optimus.encode(42) == my_other_optimus.encode(42)\nassert my_optimus.decode(my_other_optimus.encode(42)) == my_other_optimus.decode(my_optimus.encode(42))\n```\n\n**NOTE** for the generate function to work, it needs data, the data is large, and not available with the package, the data should be downloaded from [here](https://github.com/pjebs/optimus-go-primes) and the path to it is passed to the `generate` function. By default it expects the data to be in a folder called `optimus-primes` in the current working directory.\n\n```\n├── your-app.py\n├── ...\n└── optimus-primes\n \xa0\xa0 ├── p1.txt\n \xa0\xa0 ├── p2.txt\n \xa0\xa0 ├── ...\n \xa0\xa0 └── p50.txt\n```\n\nCheck the [tests](tests/) folder for test cases and other usage examples.\n\n## License\n\nThis work is licensed under\n[MIT License](https://opensource.org/licenses/MIT).\n",
    'author': 'gazorby',
    'author_email': 'gazorby@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
