# -*- coding: utf-8 -*-

from collections import OrderedDict

from democritus_lists import (
    lists_are_same_length,
    list_cycle,
    list_deduplicate,
    list_flatten,
    list_join,
    list_run_length_encoding,
    list_delete_item,
    list_item_index,
    list_count,
    lists_combine,
    list_duplicates,
    list_replace,
    list_has_index,
    list_has_mixed_types,
    list_has_single_type,
    list_item_types,
    list_item_indexes,
    list_contains_dict,
    list_sort_by_length,
    list_longest_item,
    list_shortest_item,
    list_car,
    list_cdr,
    lists_have_same_items,
    list_has_single_item,
    chunk,
)


def test_chunk_1():
    result = chunk('ABCDEFG', 3, fillvalue='x')
    assert list(result) == [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x')]

    result = chunk(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 3, fillvalue='x')
    assert list(result) == [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x')]

    result = chunk('ABCDEFG', 3)
    assert list(result) == [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', None, None)]


def test_list_has_mixed_types_1():
    assert list_has_mixed_types([0, 'a'])
    assert list_has_mixed_types([0, 'a'])
    assert not list_has_mixed_types([0, 1])
    assert not list_has_mixed_types([{}, {}])


def test_list_has_single_type_1():
    assert not list_has_single_type([0, 'a'])
    assert not list_has_single_type([0, 'a'])
    assert list_has_single_type([0, 1])
    assert list_has_single_type([{}, {}])


def test_list_has_single_item_1():
    assert not list_has_single_item([])
    assert list_has_single_item([0])
    assert list_has_single_item([0, 0])
    assert not list_has_single_item([0, 1])


def test_lists_have_same_items():
    assert lists_have_same_items([1], [1])
    assert not lists_have_same_items([1], [2])

    assert lists_have_same_items([2, 1], [1, 2])
    assert not lists_have_same_items([1], [2, 1])
    assert not lists_have_same_items([2, 1], [1])
    assert not lists_have_same_items([2, 2], [1, 2])

    assert lists_have_same_items([1, 2, 3], [3, 1, 2])
    assert not lists_have_same_items([1, 2, 3, 4], [3, 1, 2])
    assert not lists_have_same_items([1, 2, 3], [3, 1, 2, 4])
    assert not lists_have_same_items([1, 3, 3], [3, 3, 2])


def test_lists_have_same_items():
    assert lists_have_same_items([1, 2, 3], [3, 2, 1])
    assert lists_have_same_items([1, 2, 3], [3, 1, 2])
    assert not lists_have_same_items([1, 2, 3, 3], [1, 2, 2, 3])


def test_list_contains_dict_1():
    assert list_contains_dict([{'a': 1}, 1, 2, 3])
    assert not list_contains_dict([1, 2, 3])


def test_list_car_1():
    l = [1, 2, 3]
    result = list_car(l)
    assert result == 1


def test_list_cdr_1():
    l = [1, 2, 3]
    result = list_cdr(l)
    assert result == [2, 3]

    l = [0]
    result = list_cdr(l)
    assert result == []


def test_list_longest_item_1():
    l = ['a', 'aa', 'aaa']
    result = list_longest_item(l)
    assert result == 'aaa'


def test_list_longest_item_1():
    l = ['a', 'aa', 'aaa']
    result = list_shortest_item(l)
    assert result == 'a'


def test_list_sort_by_length_1():
    l = ['a', 'aa', 'aaa']
    result = list_sort_by_length(l)
    assert result == ['a', 'aa', 'aaa']

    l = ['a', 'aa', 'aaa']
    result = list_sort_by_length(l, reverse=True)
    assert result == ['aaa', 'aa', 'a']


def test_list_item_indexes_1():
    assert list_item_indexes([1, 2, 1, 2], 1) == [0, 2]
    assert list_item_indexes([1, 2, 1, 2], 2) == [1, 3]


def test_list_flatten_1():
    assert list_flatten([1, 2, 3]) == [1, 2, 3]
    assert list_flatten([1, [2], 3]) == [1, 2, 3]
    assert list_flatten([1, [2, 3]]) == [1, 2, 3]
    assert list_flatten([(1, 2), ([3, 4], [[5], [6]])]) == [1, 2, 3, 4, 5, 6]
    assert list_flatten([(1, 2), ([3, 4], [[5], [6]])], level=1) == [1, 2, [3, 4], [[5], [6]]]


def test_list_has_index_1():
    assert not list_has_index(['a', 'b', 'c'], -1)
    assert list_has_index(['a', 'b', 'c'], 0)
    assert list_has_index(['a', 'b', 'c'], 1)
    assert list_has_index(['a', 'b', 'c'], 2)
    assert not list_has_index(['a', 'b', 'c'], 3)
    assert not list_has_index(['a', 'b', 'c'], 4)
    assert not list_has_index(['a', 'b', 'c'], 4000)


def test_lists_are_same_length_1():
    l1 = ['a']
    l2 = ['b']
    l3 = ['a']
    l4 = ['a', 'b']
    l5 = []

    assert lists_are_same_length(l1, l2)
    assert lists_are_same_length(l1, l2, l3)
    assert not lists_are_same_length(l1, l2, l3, l4)
    assert not lists_are_same_length(l1, l2, l3, l4, l5)
    assert lists_are_same_length(l5)
    assert lists_are_same_length(l1)
    assert not lists_are_same_length(l1, l5)


def test_list_item_types_1():
    assert list_item_types([1, 2, 3]) == [int, int, int]
    assert list_item_types(['a', 'b', 'c']) == [str, str, str]


def test_list_replace_docs_1():
    old_list = [1, 2, 3]
    new_list = list_replace(old_list, 1, 4)
    assert new_list == [4, 2, 3]
    # test immutability
    assert old_list == [1, 2, 3]

    old_list = [1, 2, 3]
    new_list = list_replace(old_list, 5, 3)
    assert new_list == [1, 2, 3]
    # test immutability
    assert old_list == [1, 2, 3]

    old_list = [1, 1, 1]
    new_list = list_replace(old_list, 1, 0)
    assert new_list == [0, 0, 0]
    # test immutability
    assert old_list == [1, 1, 1]

    old_list = [1, 2, 3]
    new_list = list_replace(old_list, 1, 4, replace_in_place=False)
    assert new_list == [2, 3, 4]
    # test immutability
    assert old_list == [1, 2, 3]

    old_list = [1, 2, 3]
    new_list = list_replace(old_list, 1, 4)
    assert new_list == [4, 2, 3]
    # test immutability
    assert old_list == [1, 2, 3]

    old_list = [1, 2, 3]
    new_list = list_replace(old_list, 1, 4, replace_in_place=False)
    assert new_list == [2, 3, 4]
    # test immutability
    assert old_list == [1, 2, 3]

    old_list = [[1], [2, 2], [3, 3, 3]]
    new_list = list_replace(old_list, [1], [4, 4, 4, 4], replace_in_place=False)
    assert new_list == [[2, 2], [3, 3, 3], [4, 4, 4, 4]]
    # test immutability
    assert old_list == [[1], [2, 2], [3, 3, 3]]

    old_list = [[{'a': 1}], [{'b': 2}], [{'c': 3}]]
    new_list = list_replace(old_list, [{'a': 1}], [{'e': 1}])
    assert new_list == [[{'e': 1}], [{'b': 2}], [{'c': 3}]]
    # test immutability
    assert old_list == [[{'a': 1}], [{'b': 2}], [{'c': 3}]]


def test_list_deduplicate_1():
    assert list_deduplicate([1, 2, 3, 3, 3, 4, 2]) == [1, 2, 3, 4]


def test_list_deduplicate_dicts():
    assert list_deduplicate([{'a': 1}, 1, {'b': 2}]) == [{'a': 1}, 1, {'b': 2}]
    assert list_deduplicate([{'a': 1}, {'a': 1}, {'b': 2}]) == [{'a': 1}, {'b': 2}]


def test_list_duplicates():
    assert lists_have_same_items(list_duplicates([1, 2, 3, 3, 2]), [3, 2])
    assert lists_have_same_items(list_duplicates([1, 2], [2, 3]), [2])
    assert lists_have_same_items(list_duplicates([1, 2, 2], [2, 2, 3]), [2])

    assert lists_have_same_items(list_duplicates([1, 2, 3, 3, 2], deduplicate_results=False), [2, 3, 3, 2])
    assert lists_have_same_items(list_duplicates([1, 2, 2], [2, 2, 3], deduplicate_results=False), [2, 2])
    assert lists_have_same_items(list_duplicates([1, 2], [1, 2], deduplicate_results=False), [1, 2])


def test_list_run_length_encoding_1():
    assert list_run_length_encoding(['a']) == '1a'
    assert list_run_length_encoding(['a', 'a']) == '2a'
    assert list_run_length_encoding(['a', 'b']) == '1a1b'
    assert list_run_length_encoding(['a', 'a', 'b']) == '2a1b'
    assert list_run_length_encoding(['a', 'b', 'b']) == '1a2b'
    assert list_run_length_encoding(['a', 'b', 'a']) == '1a1b1a'


def test_list_run_length_encoding_2():
    assert list_run_length_encoding(['aa']) == '1aa'
    assert list_run_length_encoding(['aa', 'aa']) == '2aa'
    assert list_run_length_encoding(['aa', 'bbb']) == '1aa1bbb'
    assert list_run_length_encoding(['aa', 'aa', 'bbb']) == '2aa1bbb'
    assert list_run_length_encoding(['aa', 'bbb', 'bbb']) == '1aa2bbb'
    assert list_run_length_encoding(['aa', 'bbb', 'aa']) == '1aa1bbb1aa'
    assert (
        list_run_length_encoding('WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW')
        == '12W1B12W3B24W1B14W'
    )


def test_multiple_list_duplicates():
    assert list_duplicates([1, 2, 3, 3, 2], [1, 3, 4, 5]) == [1, 3]
    assert list_duplicates(set([1, 2, 3]), set([3, 5, 6])) == [3]


def test_lists_combine_1():
    assert lists_combine([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]
    assert lists_combine([1, 2, 3], [4, 5, 6], [7], [8, 9]) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_list_count_1():
    assert list_count([1, 2, 3, 2, 3]) == OrderedDict([(1, 1), (2, 2), (3, 2)])
    assert list_count(['bob', 'bob', 'frank', 'bob', 'john', 'frank', 'tim', 'tim']) == OrderedDict(
        [('john', 1), ('frank', 2), ('tim', 2), ('bob', 3)]
    )


def test_list_item_index_1():
    assert list_item_index(['a', 'b'], 'a') == 0
    assert list_item_index(['a', 'b'], 'b') == 1
    assert list_item_index(['a', 'b'], 'c') == -1


def test_list_cycle_1():
    l = list_cycle([1, 2, 3], length=42)
    assert len(l) == 42
    assert l[0] == 1
    assert l[1] == 2
    assert l[2] == 3
    assert l[3] == 1


def test_list_delete_item_1():
    assert list_delete_item([1, 2, 3, 3, 2, 3, 2], 2) == [1, 3, 3, 3]
    assert list_delete_item([1, 'b', {'a': 'b'}, 'b'], 'b') == [1, {'a': 'b'}]
    assert list_delete_item([1, 'b', {'a': 'b'}, 'b'], {'a': 'b'}) == [1, 'b', 'b']


def test_list_join_1():
    assert list_join([1, 2, 3]) == '1,2,3'
    assert list_join([1, 2, 3], '') == '123'
    assert list_join(['a', 'b', {}], '/') == 'a/b/{}'
    assert list_join(['a', 'b', {}], '//') == 'a//b//{}'
