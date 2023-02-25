
import re


def remove_leading(value):
    return re.sub(r'^\d+\. ', '', value)
