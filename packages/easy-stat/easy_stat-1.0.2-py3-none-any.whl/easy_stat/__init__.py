from math import sqrt
from typing import Any, overload
from matplotlib import pyplot

class DescriptiveStatistics:

    original_data: list[int | float] | dict[Any, int | float] = None
    numerical_data: list[int | float] = []

    @overload
    def __init__(self, data: list[int | float]) -> None: ...

    @overload
    def __init__(self, data: dict[Any, int | float]) -> None: ...

    def __init__(self, data: list[int | float] | dict[Any, int | float]) -> None:
        if isinstance(data, list) and all(isinstance(x, int | float) for x in data):
            self.original_data = data
            self.numerical_data = data
        elif isinstance(data, dict) and all(isinstance(data[x], int | float) for x in data):
            self.original_data = data
            self.numerical_data = list(data.values())
        else:
            raise Exception("Unsupportable data type")

    @property
    def min(self) -> int | float:
        return min(self.numerical_data)

    @property
    def max(self) -> int | float:
        return max(self.numerical_data)

    @property
    def sum(self) -> int | float:
        return sum(self.numerical_data)

    @property
    def mean(self) -> float:
        return float(sum(self.numerical_data) / len(self.numerical_data))

    @property
    def median(self) -> float:
        sorted_data: list[int | float] = sorted(self.numerical_data)
        if len(sorted_data) % 2 == 0:
            return float((sorted_data[int(len(sorted_data) / 2) - 1] + sorted_data[int(len(sorted_data) / 2)]) / 2)
        else:
            return float(sorted_data[int(len(sorted_data) / 2)])

    @property
    def mode(self) -> list[int | float]:
        mode: list[int | float] = []
        max_count: int = 0
        levels: int = -1
        element: int | float = self.numerical_data[0]
        counter: int = 1
        for i in range(1, len(self.numerical_data)):
            if self.numerical_data[i] == element:
                counter += 1
            else:
                if counter == max_count:
                    mode.append(element)
                elif counter > max_count:
                    max_count = counter
                    mode = [element] 
                    levels += 1
                element = self.numerical_data[i]
                counter = 1
        if counter == max_count:
            mode.append(element)
        elif counter > max_count:
            max_count = counter
            mode = [element] 
            levels += 1
        return mode if levels != 0 else []

    @property
    def range(self) -> float:
        return float(max(self.numerical_data) - min(self.numerical_data))

    @property
    def variance(self) -> float:
        mean: float = self.mean
        variance_sum: int = 0
        for d in self.numerical_data:
            variance_sum += (d - mean) ** 2
        return float(variance_sum / len(self.numerical_data))

    @property
    def standard_deviation(self) -> float:
        return float(sqrt(self.variance))

    def show_frequency(self) -> None:
        print("Made with matplotlib")
        pyplot.hist(self.numerical_data)
        pyplot.show()

    def show_histogram(self) -> None:
        print("Made with matplotlib")
        if isinstance(self.original_data, list):
            pyplot.bar([i for i in range(0, len(self.numerical_data))], self.numerical_data)
            pyplot.show()
        elif isinstance(self.original_data, dict):
            pyplot.bar(list(self.original_data.keys()), self.numerical_data)
            pyplot.show()

    def show_changing(self) -> None:
        print("Made with matplotlib")
        if isinstance(self.original_data, list):
            pyplot.plot([i for i in range(0, len(self.numerical_data))], self.numerical_data)
            pyplot.show()
        elif isinstance(self.original_data, dict):
            pyplot.plot(list(self.original_data.keys()), self.numerical_data)
            pyplot.show()