# coding: utf-8

#
# Utility functions for handling dict, list, tuple variable
#
# @copyright  2017 guenbakku
# @license    MIT
#

def get(arr, path):
    ''' Return value of item provided in path from a list, tuple or dict '''
    if isinstance(path, list):
        parts = path
    elif isinstance(path, str):
        parts = path.split('.')
    else:
        raise TypeError('type of path must be str or dict.')

    part = parts.pop(0)
    if isinstance(arr, (list, tuple)):
        try: 
            part = int(part)
        except ValueError:
            return None
        if part > len(arr) - 1 or part < -len(arr):
            return None
    elif isinstance(arr, dict):
        if part not in arr:
            return None
    else:
        return None

    if len(parts) > 0:
        return get(arr[part], parts)
    else:
        return arr[part]


def insert(aDict, path, val):
    ''' Insert value into aDict follow by path '''
    if not isinstance(aDict, dict):
        raise TypeError('type of item provided in path must be dict: %s.' % path)

    if isinstance(path, list):
        parts = path
    elif isinstance(path, str):
        parts = path.split('.')
    else:
        raise TypeError('type of path must be str or dict.')

    part = parts.pop(0)
    if len(parts) > 0:
        if part not in aDict:
            aDict[part] = {}
        if isinstance(aDict[part], dict):
            aDict[part].update(insert(aDict[part], parts, val))
        else:
            aDict[part] = insert(aDict[part], parts, val)
    else:
        if part not in aDict:
            aDict[part] = val
        elif isinstance(aDict[part], list):
            aDict[part].append(val)
        elif isinstance(aDict[part], dict) and isinstance(val, dict):
            aDict[part].update(val)
        else:
            aDict[part] = val
    return aDict
