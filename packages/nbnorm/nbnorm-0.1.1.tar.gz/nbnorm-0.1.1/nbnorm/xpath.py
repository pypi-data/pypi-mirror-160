import sys


def xpath(top, path):
    """
    navigates a nested data structure 'top' and returns the subpart corresponding to path
    path is either an iterable, or a string with steps separated with a .
    raise an exection if path s not present
    examples
    xpath({'a': 1, 'b': [{'c': 1, 'd': 1000}, {'c': 2, 'd': 2000}]},
          ['b', 0, 'd']) -> 1000
    xpath({'a': {'x': 10, 'y': {'z': 1000}}, 'b': [{'c': 1, 'd': 1000}, {'c': 2, 'd': 2000}]},
          "a.y.z")
           -> 1000
    """
    result = top
    if isinstance(path, str):
        path = path.split('.')
    for step in path:
        result = result[step]
    return result

def xpath_create(top, path, leaf_type):
    """
    like xpath but create empty entries in the structure for missing steps
    (except for int steps that are meaningful in lists only)

    leaf_type specifies the type of the empty leaf created when the path is missing

    examples
      top = {}
      xpath_create(top, 'metadata.nbhosting.title', str) -> None
      BUT afterwards top has changed to
      {'metadata': {'nbhosting': {'title': ""}}}
    """
    result = top
    if isinstance(path, str):
        path = path.split('.')
    for index, step in enumerate(path):
        if isinstance(step, int):
            result = result[step]
        else:
            if step not in result:
                result[step] = leaf_type() if (index == len(path) - 1) else {}
            result = result[step]
    return result
