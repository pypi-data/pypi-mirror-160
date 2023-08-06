# Python Performance toolt & utilities

![License](https://img.shields.io/badge/License-Apache2-SUCCESS)
![Pypi](https://img.shields.io/pypi/v/python-performance-tools)
![Python Versions](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue)

In a nutshell ``Python performance tools`` is a small library with a set of utilities to help you measure and analyze the performance of your code.

# Install

```bash
> pip install python-performance-tools
```

# Usage examples

**Example 1**

```python
# File: example_1.py

import os
import time

from performance_tools import *


def main():
    environment = os.environ.get("ENVIRONMENT", None)

    with catch_time("Example message 2", lambda: environment in ("DEVELOPMENT", "STAGING")):
        for i in range(10):
            time.sleep(1)


if __name__ == '__main__':
    main()

```

After running the code, you will see:

```bash
> python examples/example_1.py
Time: 1.021636976 :: Example message
```

**Example 2**

```python
# File: example_2.py

import os
import time

from performance_tools import *


def main():
    environment = os.environ.get("ENVIRONMENT", "STAGING")

    with catch_time("Example message 2", lambda: environment in ("DEVELOPMENT", "STAGING")):
        for i in range(10):
            time.sleep(0.1)


if __name__ == '__main__':
    main()

```

After running the code, you will see:

```bash
> export ENVIRONMENT=DEVELOPMENT
> python examples/example_2.py
Time: 1.035312797 :: Example message 2
```

# License

Dictionary Search is Open Source and available under the [MIT](https://github.com/cr0hn/python-performance-tools/blob/main/LICENSE).

# Contributions

Contributions are very welcome. See [CONTRIBUTING.md](https://github.com/cr0hn/python-performance-tools/blob/main/CONTRIBUTING.md) or skim existing tickets to see where you could help out.


