from math import ceil
from csv import DictWriter
import os


def partial(data, parts_count):
    part_len = ceil((len(data) / parts_count))
    result = []
    for i in range(0, len(data), part_len):
        result.append(data[i:i+part_len])
    return result


def write_csv(filename, data, order):
    with open(filename, 'a') as file:
        writer = DictWriter(file, fieldnames=order)
        is_empty = os.stat(filename).st_size == 0
        if is_empty:
            writer.writeheader()
        writer.writerow(data)
