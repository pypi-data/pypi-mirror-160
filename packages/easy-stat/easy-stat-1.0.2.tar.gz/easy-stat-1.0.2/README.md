# easy-statistics

**GitHub:** https://github.com/s0urcedev/easy-stat

**PyPi:** https://pypi.org/project/easy-stat

Python module for statistics

## Installation:

```console
pip install easy-statistics
```

## Importing:

```py
from easy_stat import DescriptiveStatistics
```

## Using:

`DescriptiveStatistics()` — create `DescriptiveStatistics` object from list of ints or floats or from dictionary of ints or floats with any keys

`min` — property with minimal value

`max` — property with maximal value

`sum` — property with sum of values

`mean` — property with data mean

`median` — property with data median

`mode` — property with data mode (`[]` in return says that there isn't mode in your data)

`range` — property with data range

`variance` — property with data variance

`standard_deviation` — property with data standard_deviation

`show_frequency` — show graph of values frequency

`show_histogram` — show histogram of data connected to keys

`show_changing` — show graph of values changing connected to keys

All graphs made with [matplotlib](https://github.com/matplotlib/matplotlib)
