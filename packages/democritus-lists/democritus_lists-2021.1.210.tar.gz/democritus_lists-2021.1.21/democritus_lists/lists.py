from typing import Any, Union, List, Dict, Iterable, Tuple

# TODO: consider applying @decorators.listify_first_arg argument to all/most functions in this module


def list_sort_by_length(list_arg: List[Any], **kwargs) -> List[Any]:
    """."""
    sorted_list = sorted(list_arg, key=lambda x: len(x), **kwargs)
    return sorted_list


def list_longest_item(list_arg: List[Any]) -> Any:
    """."""
    longest_item = list_sort_by_length(list_arg, reverse=True)[0]
    return longest_item


def lists_interleave(*iterables):
    """."""
    import more_itertools

    # TODO: more_itertools also has an interleave option, but I've chosen not to use that one; may want to provide an option to stop once an iterable is exhausted
    return listify(more_itertools.interleave_longest(*iterables))


# TODO: rename this as "shortest" and move it to an iterable file?
def list_shortest_item(list_arg: list) -> Any:
    """."""
    shortest_item = list_sort_by_length(list_arg)[0]
    return shortest_item


def list_flatten(list_arg: list, level: int = None, **kwargs) -> list:
    """Flatten all items in the list_arg so that they are all items in the same list."""
    import more_itertools

    return listify(more_itertools.collapse(list_arg, levels=level, **kwargs))


def listify(iterable):
    """Convert the given iterable into a list - useful for generators and other items like CSV readers."""
    return [i for i in iterable]


def list_car(list_arg: list) -> Any:
    return list_arg[0]


def list_cdr(list_arg: list) -> list:
    return list_arg[1:]


def list_has_index(list_: list, index: Union[str, int]):
    """."""
    index_int = int(index)
    if index_int >= 0 and index_int <= len(list_) - 1:
        return True
    else:
        return False


def chunk(iterable: Iterable, chunk_size: int, *, fillvalue: Any = None):
    """."""
    import more_itertools

    return more_itertools.grouper(iterable, chunk_size, fillvalue=fillvalue)


def list_item_types(list_arg: list) -> List[str]:
    """Return a set containing the types of all items in the list_arg."""
    # TODO: I don't like the fact that this function returns types as a string (see also the dict_key_types function)
    types = [type(item) for item in list_arg]
    return types


# # TODO: I made a change to the list_item_types function to return the type rather than the string... this will break some of the functions below. Need to update them


# TODO: should I create other functions like this one?
def list_contains_dict(list_arg: list) -> bool:
    """Return whether or not the given list_arg contains a dict."""
    list_arg_types = list_item_types(list_arg)
    return dict in list_arg_types


def list_contains_list(list_arg: list) -> bool:
    """Return whether or not the given list_arg contains a list."""
    list_arg_types = list_item_types(list_arg)
    return list in list_arg_types


def list_deduplicate(list_arg: list) -> list:
    """Deduplicate the list_arg."""
    if list_contains_dict(list_arg) or list_contains_list(list_arg):
        deduplicated_list = []
        for i in list_arg:
            if i not in deduplicated_list:
                deduplicated_list.append(i)
    else:
        # TODO: will this work for every type except for dicts???
        deduplicated_list = list(set(list_arg))
    return deduplicated_list


def list_cycle(list_arg: list, length: Union[int, None] = None) -> list:
    """Cycle through the list_arg as much as needed."""
    import itertools

    if length is None:
        return itertools.cycle(list_arg)
    else:
        full_cycle = list_cycle(list_arg, None)
        partial_cycle = []
        for index, item in enumerate(full_cycle):
            partial_cycle.append(item)
            if index == length - 1:
                break
        return partial_cycle


# TODO: rename this function
def list_delete_empty_items(list_arg: list) -> list:
    """Delete items from the list_arg is the item is an empty strings, empty list, zero, False or None."""
    empty_values = ('', [], 0, False, None)
    # TODO: not sure if this is the right way to implement this
    return [i for i in list_arg if i not in empty_values]


def lists_have_same_items(a: List[Any], b: List[Any], *args: List[Any]) -> bool:
    """See if the lists have identical items."""
    first_list = a
    remaining_lists = [b]
    remaining_lists.extend(listify(args))

    if lists_are_same_length(a, b) and lists_are_same_length(*remaining_lists):
        for item in first_list:
            first_list_count = first_list.count(item)
            item_counts = [list_.count(item) for list_ in remaining_lists]
            monotonic_list = list_has_single_item(item_counts)
            same_count = list_car(item_counts) == first_list_count
            if not monotonic_list or not same_count:
                return False
        return True
    else:
        return False


def lists_are_same_length(*args: list, debug_failure: bool = False) -> bool:
    """Return whether or not the given lists are the same lengths."""
    from democritus_dicts import dict_values

    lengths = list(map(len, args))
    result = list_has_single_item(lengths)

    if debug_failure and not result:
        list_length_breakdown = list_count(lengths)
        minority_list_count = min(dict_values(list_length_breakdown))
        for index, arg in enumerate(args):
            if list_length_breakdown[len(arg)] == minority_list_count:
                print(f'Argument {index} is not the same length as the majority of the arguments')

    return result


def list_has_single_item(list_arg: list) -> bool:
    """Return whether or not the items of the given list_arg are the same."""
    list_arg = list_deduplicate(list_arg)
    result = len(list_arg) == 1
    return result


def list_run_length_encoding(list_arg: list) -> str:
    """Perform run-length encoding on the given array. See https://en.wikipedia.org/wiki/Run-length_encoding for more details."""
    encodings = []

    for i in list_arg:
        if len(encodings) > 0 and i == encodings[-1]['value']:
            encodings[-1]['length'] += 1
        else:
            encodings.append({'value': i, 'length': 1})

    return ''.join(['{}{}'.format(entry['length'], entry['value']) for entry in encodings])


def list_count(list_arg: list) -> Dict[Any, int]:
    """Count each item in the iterable."""
    from democritus_dicts import dict_sort_by_values

    count = {}
    for i in list_arg:
        count[i] = count.get(i, 0) + 1
    count = dict_sort_by_values(count)
    return count


def list_item_index(list_arg: list, item: Any) -> int:
    """Find the given item in the iterable. Return -1 if the item is not found."""
    try:
        return list_arg.index(item)
    except ValueError:
        return -1


def list_item_indexes(list_arg: list, item: Any) -> Tuple[int, ...]:
    """Find the given item in the iterable. Return -1 if the item is not found."""
    indexes = [index for index, value in enumerate(list_arg) if value == item]
    return indexes


def list_duplicates(list_a: list, list_b: list = None, *, deduplicate_results: bool = True) -> list:
    """Find duplicates. If deduplicate_results is False, all instances of a duplicate will be added to the resulting list."""
    if list_b is not None:
        if deduplicate_results:
            return list(set(list_a).intersection(set(list_b)))
        else:
            duplicates = []
            for item in list_a:
                if list_b.count(item) > 0:
                    duplicates.append(item)
            return duplicates
    else:
        # TODO: I used to use pydash, but have removed it to simplify the required packages
        # import pydash.arrays
        # return pydash.arrays.duplicates(list_a)
        duplicates = []
        for item in list_a:
            if list_a.count(item) > 1:
                duplicates.append(item)

        if deduplicate_results:
            return list_deduplicate(duplicates)
        else:
            return duplicates


def list_has_item_of_type(list_arg: list, type_arg) -> bool:
    """Return whether or not there is at least one item of the type specified by the type_arg in the list_arg."""
    return type_arg in list_item_types(list_arg)


def list_has_all_items_of_type(list_arg: list, type_arg) -> bool:
    """Return whether or not all items in list_arg are of the type specified by the type_arg."""
    item_types = list_item_types(list_arg)
    result = item_types[0] == type_arg and list_has_single_item(item_types)
    return result


def list_has_mixed_types(list_arg: list) -> bool:
    """Return whether or not the list_arg has items with two or more types."""
    return len(list_deduplicate(list_item_types(list_arg))) >= 2


def list_has_single_type(list_arg: list) -> bool:
    """Return whether or not the list_arg has items of only one type."""
    return len(list_deduplicate(list_item_types(list_arg))) == 1


def list_join(list_arg: list, join_characters: str = ',') -> str:
    string_list = [str(item) for item in list_arg]
    return join_characters.join(string_list)


def lists_combine(list_a: list, list_b: list, *args: list) -> list:
    """Combine list_a, list_b, and any args into one list."""
    list_a.extend(list_b)
    for list_ in args:
        list_a.extend(list_)
    return list_a


# TODO: consider renaming this to `list_delete_all_instances_of_item`
def list_delete_item(list_arg: list, item_to_delete: Any) -> list:
    """Remove all instances of the given item_to_delete from the list_arg."""
    from itertools import filterfalse

    result = listify(filterfalse(lambda x: x == item_to_delete, list_arg))
    return result


def list_replace(list_arg: list, old_value, new_value, *, replace_in_place: bool = True) -> list:
    """Replace all instances of the old_value with the new_value in the given list_arg."""
    old_value_indexes = list_item_indexes(list_arg, old_value)
    new_list = list_delete_item(list_arg, old_value)

    for index in old_value_indexes:
        if replace_in_place:
            new_list.insert(index, new_value)
        else:
            new_list.append(new_value)

    return new_list


# def list_entropy(list_arg: list):
#     """Find the entropy of the items in the given list."""
#     import math
#     from nlp import frequencyDistribution

#     freqdist = frequencyDistribution(iterable)
#     probs = [freqdist.freq(l) for l in freqdist]
#     return -sum(p * math.log(p, 2) for p in probs)
