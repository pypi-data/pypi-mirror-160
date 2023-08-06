import pytest

from democritus_math import (
    number_closest,
    number_furthest,
    cartesian_product,
    sympy_symbol,
    equation_solve,
    one_cold_encode,
    one_hot_encode,
    is_integer_tuple,
    decimal_to_gray_code,
    gray_code_to_decimal,
    decimal_to_hex,
    hex_to_decimal,
    roman_numeral_to_decimal,
    decimal_to_roman_numeral,
    integer_tuple_to_decimal,
    integer_to_decimal,
    decimal_to_base,
    outer_division,
    outer_product,
    multiplication_table,
    number_evenly_divides,
    number_evenly_divided_by,
    fraction_examples,
    iterable_differences,
    combinations,
    combinations_with_replacement,
    permutations,
    fraction_simplify,
    remainder,
    floor,
    ceiling,
    factorial,
    fraction_complex_to_mixed_fraction,
    fraction_mixed_to_complex_fraction,
    dot_product,
    percent,
    gcd,
    ratio,
    transpose,
    number_line,
    integer_tuple,
    fibonacci,
    fibonacci_sequence,
    expression_explore,
    prod,
)
from democritus_math.maths import _hot_or_cold_encoder, _split_fraction, _split_mixed_fraction, _base_converter_init

# from democritus_numbers import number_is_approx

x = sympy_symbol('x')
y = sympy_symbol('y')


def test_expression_explore_docs_1():
    result = expression_explore('x + 1', ['x'], 0, 10, 1)
    assert list(result) == [
        (0, [-1]),
        (1, [0]),
        (2, [1]),
        (3, [2]),
        (4, [3]),
        (5, [4]),
        (6, [5]),
        (7, [6]),
        (8, [7]),
        (9, [8]),
    ]


def test_fibonacci_docs_1():
    result = fibonacci(5)
    assert result == 8


def test_fibonacci_sequence_docs_1():
    result = fibonacci_sequence(5)
    assert result == [1, 1, 2, 3, 5]


# def test__base_converter_init_docs_1():
#     assert _base_converter_init('alphabet') == 'fill'  # fill


# def test__hot_or_cold_encoder_docs_1():
#     assert _hot_or_cold_encoder('items', 'default_value', 'changed_value', reverse=NameConstant) == 'fill'  # fill


# def test__split_fraction_docs_1():
#     assert _split_fraction('fraction_string') == 'fill'  # fill


# def test__split_mixed_fraction_docs_1():
#     assert _split_mixed_fraction('fraction_string') == 'fill'  # fill


def test_cartesian_product_docs_1():
    assert cartesian_product('abc') == [('a',), ('b',), ('c',)]
    assert cartesian_product('abc', 'abc') == [
        ('a', 'a'),
        ('a', 'b'),
        ('a', 'c'),
        ('b', 'a'),
        ('b', 'b'),
        ('b', 'c'),
        ('c', 'a'),
        ('c', 'b'),
        ('c', 'c'),
    ]
    assert cartesian_product('abc', repeat=2) == [
        ('a', 'a'),
        ('a', 'b'),
        ('a', 'c'),
        ('b', 'a'),
        ('b', 'b'),
        ('b', 'c'),
        ('c', 'a'),
        ('c', 'b'),
        ('c', 'c'),
    ]
    assert cartesian_product([0, 1], [2, 3], [4, 5]) == [
        (0, 2, 4),
        (0, 2, 5),
        (0, 3, 4),
        (0, 3, 5),
        (1, 2, 4),
        (1, 2, 5),
        (1, 3, 4),
        (1, 3, 5),
    ]


def test_ceiling_docs_1():
    assert ceiling(1.2) == 2
    assert ceiling(1.9) == 2
    assert ceiling(2) == 2


def test_combinations_docs_1():
    assert combinations('ab') == [('a',), ('b',), ('a', 'b')]
    assert combinations('a') == [('a',)]
    assert combinations('ab', length=1) == [('a',), ('b',)]


def test_combinations_with_replacement_docs_1():
    assert combinations_with_replacement('ab') == [
        ('a',),
        ('b',),
        ('a', 'a'),
        ('a', 'b'),
        ('b', 'b'),
    ]
    assert combinations_with_replacement('abc', length=2) == [
        ('a', 'a'),
        ('a', 'b'),
        ('a', 'c'),
        ('b', 'b'),
        ('b', 'c'),
        ('c', 'c'),
    ]
    assert combinations_with_replacement([1, 2, 3]) == [
        (1,),
        (2,),
        (3,),
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 2),
        (2, 3),
        (3, 3),
        (1, 1, 1),
        (1, 1, 2),
        (1, 1, 3),
        (1, 2, 2),
        (1, 2, 3),
        (1, 3, 3),
        (2, 2, 2),
        (2, 2, 3),
        (2, 3, 3),
        (3, 3, 3),
    ]


def test_decimal_to_base_docs_1():
    assert decimal_to_base(3, 1) == integer_tuple(base=1, digits=(1, 1, 1))
    assert decimal_to_base(3, 2) == integer_tuple(base=2, digits=(1, 1))
    assert decimal_to_base(3, 3) == integer_tuple(base=3, digits=(1, 0))
    assert decimal_to_base(3, 4) == integer_tuple(base=4, digits=(3,))
    assert decimal_to_base(254, 256) == integer_tuple(base=256, digits=(254,))
    assert decimal_to_base(255, 256) == integer_tuple(base=256, digits=(255,))
    assert decimal_to_base(256, 256) == integer_tuple(base=256, digits=(1, 0))
    assert decimal_to_base(257, 256) == integer_tuple(base=256, digits=(1, 1))
    assert decimal_to_base(260, 256) == integer_tuple(base=256, digits=(1, 4))
    assert decimal_to_base(12322322, 256) == integer_tuple(base=256, digits=(188, 6, 18))
    assert decimal_to_base(65793, 256) == integer_tuple(base=256, digits=(1, 1, 1))


def test_decimal_to_gray_code_docs_1():
    assert decimal_to_gray_code(0) == integer_tuple(base=2, digits=(0,))
    assert decimal_to_gray_code(1) == integer_tuple(base=2, digits=(1,))
    assert decimal_to_gray_code(2) == integer_tuple(base=2, digits=(1, 1))
    assert decimal_to_gray_code(3) == integer_tuple(base=2, digits=(1, 0))
    assert decimal_to_gray_code(4) == integer_tuple(base=2, digits=(1, 1, 0))
    assert decimal_to_gray_code(5) == integer_tuple(base=2, digits=(1, 1, 1))
    assert decimal_to_gray_code(6) == integer_tuple(base=2, digits=(1, 0, 1))
    assert decimal_to_gray_code(7) == integer_tuple(base=2, digits=(1, 0, 0))
    assert decimal_to_gray_code(8) == integer_tuple(base=2, digits=(1, 1, 0, 0))
    assert decimal_to_gray_code(9) == integer_tuple(base=2, digits=(1, 1, 0, 1))
    assert decimal_to_gray_code(10) == integer_tuple(base=2, digits=(1, 1, 1, 1))
    assert decimal_to_gray_code(11) == integer_tuple(base=2, digits=(1, 1, 1, 0))
    assert decimal_to_gray_code(12) == integer_tuple(base=2, digits=(1, 0, 1, 0))
    assert decimal_to_gray_code(13) == integer_tuple(base=2, digits=(1, 0, 1, 1))
    assert decimal_to_gray_code(14) == integer_tuple(base=2, digits=(1, 0, 0, 1))
    assert decimal_to_gray_code(15) == integer_tuple(base=2, digits=(1, 0, 0, 0))
    assert decimal_to_gray_code('0') == integer_tuple(base=2, digits=(0,))
    assert decimal_to_gray_code('1') == integer_tuple(base=2, digits=(1,))
    assert decimal_to_gray_code(integer_tuple(base=10, digits=(2,))) == integer_tuple(base=2, digits=(1, 1))


# def test_decimal_to_hex_docs_1():
#     assert decimal_to_hex('decimal_number') == 'fill'  # fill


def test_decimal_to_roman_numeral_docs_1():
    assert decimal_to_roman_numeral(7) == 'VII'
    assert decimal_to_roman_numeral(9) == 'IX'


def test_dot_product_docs_1():
    assert dot_product([1, 3, -5], [4, -2, -1]) == 3
    assert dot_product([10, 10], [20, 20]) == 400


def test_equation_solve_docs_1():
    assert equation_solve('x-2', ['x']) == [2]
    assert equation_solve('x + y - 1', ['x', 'y']) == [{x: 1 - y}]
    assert number_is_approx(equation_solve('Eq(tan(x), 2.348)', ['x'])[0], 1.16816837693881)


def test_factorial_docs_1():
    assert factorial(3) == 6
    assert factorial(4) == 24


def test_floor_docs_1():
    assert floor(1.2) == 1
    assert floor(1.9) == 1
    assert floor(2) == 2


def test_fraction_complex_to_mixed_fraction_docs_1():
    assert fraction_complex_to_mixed_fraction('8/6') == '1 1/3'
    assert fraction_complex_to_mixed_fraction('8/8') == '1'
    assert fraction_complex_to_mixed_fraction('6/8') == '3/4'


# def test_fraction_examples_docs_1():
#     assert fraction_examples(fractions_as_strings=NameConstant, n=Num) == 'fill'  # fill


def test_fraction_mixed_to_complex_fraction_docs_1():
    assert fraction_mixed_to_complex_fraction('1 1/3') == '4/3'
    assert fraction_mixed_to_complex_fraction('3/4') == '3/4'


def test_fraction_simplify_docs_1():
    assert fraction_simplify('6/8') == '3/4'
    assert fraction_simplify('8/6') == '4/3'
    assert fraction_simplify('18/6') == '3/1'
    assert fraction_simplify('24/528') == '1/22'
    assert fraction_simplify('2/7') == '2/7'
    assert fraction_simplify('7/2') == '7/2'

    # test with bad data
    with pytest.raises(ValueError):
        assert fraction_simplify('foo') == 'fill'


# def test_gcd_docs_1():
#     assert gcd('number1', 'number2') == 'fill'  # fill


def test_gray_code_to_decimal_docs_1():
    assert gray_code_to_decimal(integer_tuple(base=2, digits=(1, 1))) == 2
    assert gray_code_to_decimal(integer_tuple(base=2, digits=(1, 0, 0, 0))) == 15


# def test_hex_to_decimal_docs_1():
#     assert hex_to_decimal('hex') == 'fill'  # fill


def test_integer_to_decimal_docs_1():
    assert integer_to_decimal(10, 2) == 2
    assert integer_to_decimal('10', 2) == 2
    assert integer_to_decimal(10, 3) == 3
    assert integer_to_decimal(10, 4) == 4


def test_integer_tuple_to_decimal_docs_1():
    assert integer_tuple_to_decimal(integer_tuple(base=2, digits=(1, 1))) == 3
    assert integer_tuple_to_decimal(integer_tuple(base=3, digits=(1, 1, 0, 1))) == 37
    assert integer_tuple_to_decimal(integer_tuple(base=10, digits=(9, 0))) == 90


def test_is_integer_tuple_docs_1():
    assert is_integer_tuple(integer_tuple(base=2, digits=(1, 1))) == True
    assert is_integer_tuple((1, 1)) == False
    assert is_integer_tuple(1) == False


def test_iterable_differences_docs_1():
    assert iterable_differences([1, 2, 3]) == [-4, -4, -2, -2, 0, 0]


def test_multiplication_table_docs_1():
    assert multiplication_table(3, 3) == [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
    assert multiplication_table(3, 3, a_start=2, b_start=2) == [[4, 6], [6, 9]]


def test_number_closest_docs_1():
    assert number_closest(0, 1, 2) == 1
    assert number_closest(-1, 0, -5) == -1
    assert number_closest(1.1, 1.5, 1.1) == 1.1


def test_number_evenly_divided_by_docs_1():
    assert number_evenly_divided_by(10, 1) == True
    assert number_evenly_divided_by(10, 2) == True
    assert number_evenly_divided_by(10, 5) == True
    assert number_evenly_divided_by(10, 7) == False
    assert number_evenly_divided_by(10, 10) == True
    # assert number_evenly_divided_by(10, 0) == integer division or modulo by zero


def test_number_evenly_divides_docs_1():
    assert number_evenly_divides(1, 10) == True
    assert number_evenly_divides(2, 10) == True
    assert number_evenly_divides(5, 10) == True
    assert number_evenly_divides(7, 10) == False
    assert number_evenly_divides(10, 10) == True
    # assert number_evenly_divides(0, 10) == integer division or modulo by zero


def test_number_furthest_docs_1():
    assert number_furthest(0, 1, 2) == 0
    assert number_furthest(-1, 0, -5) == 0
    assert number_furthest(1.1, 1.5, 1.1) == 1.5


def test_number_line_docs_1():
    assert number_line(8.5, 0, 10, interval=0.5) == '0................|..10'
    assert number_line(6, 5, 10, interval=1) == '5|...10'
    assert number_line(6, 5, 10, interval=0.5) == '5.|.......10'
    assert number_line(2, 1, 3, interval=1) == '1|3'
    assert number_line(11, 10, 12, interval=1) == '10|12'
    assert number_line(0, -1, 1, interval=0.5) == '-1.|.1'
    assert number_line(0, -2, 1, interval=0.25) == '-2.......|...1'
    assert number_line(-1, -2, 1, interval=0.25) == '-2...|.......1'
    assert number_line(-2, -3, -1, interval=1) == '-3|-1'
    assert number_line(-8, -10, -5, interval=0.5) == '-10...|.....-5'
    assert number_line(1, -1, 1, interval=1) == '-1.|(1)'
    assert number_line(1, 1, 2) == '(1)|2'
    assert number_line(1, 1, 10) == '(1)|........10'
    assert number_line(10, 1, 10) == '1........|(10)'
    with pytest.raises(RuntimeError):
        number_line(1, 10, 1, interval=1)
    with pytest.raises(RuntimeError):
        number_line(11, 1, 10, interval=1)


def test_one_cold_encode_docs_1():
    assert one_cold_encode([True, False, True]) == [[1, 0], [0, 1], [1, 0]]
    assert one_cold_encode([2, 1, 1, 2, 5, 3]) == [
        [1, 0, 1, 1],
        [0, 1, 1, 1],
        [0, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 1, 0],
        [1, 1, 0, 1],
    ]
    assert one_cold_encode([True, False, True], reverse=True) == [[0, 1], [1, 0], [0, 1]]


def test_one_hot_encode_docs_1():
    assert one_hot_encode([True, False, True]) == [[0, 1], [1, 0], [0, 1]]
    assert one_hot_encode([2, 1, 1, 2, 5, 3]) == [
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ]
    assert one_hot_encode([True, False, True], reverse=True) == [[1, 0], [0, 1], [1, 0]]


# def test_outer_division_docs_1():
#     assert outer_division() == 'fill'  # fill


def test_outer_product_docs_1():
    assert outer_product(2, 3) == [[1, 2, 3], [2, 4, 6]]
    assert outer_product(3, 2) == [[1, 2], [2, 4], [3, 6]]
    assert outer_product(3, 3) == [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
    assert outer_product(3, 3, a_start=2) == [[2, 4, 6], [3, 6, 9]]
    assert outer_product(3, 3, b_start=3) == [[3], [6], [9]]


# def test_percent_docs_1():
#     assert percent('ratio') == 'fill'  # fill


# def test_permutations_docs_1():
#     assert permutations('iterable', length=NameConstant) == 'fill'  # fill


def test_prod_docs_1():
    assert prod([1, 2, 3, 4]) == 24
    assert prod([1, '2', 3, '4']) == 24


def test_ratio_docs_1():
    assert ratio(5, 10) == '1:2'
    assert ratio(2, 20) == '1:10'
    assert ratio(12, 13) == '12:13'


# def test_remainder_docs_1():
#     assert remainder('dividend', 'divisor') == 'fill'  # fill


def test_roman_numeral_to_decimal_docs_1():
    assert roman_numeral_to_decimal('vii') == 7
    assert roman_numeral_to_decimal('ix') == 9
    assert roman_numeral_to_decimal('iX') == 9
    assert roman_numeral_to_decimal('Ix') == 9
    assert roman_numeral_to_decimal('IX') == 9


def test_sympy_symbol_docs_1():
    assert sympy_symbol('x') == x


def test_transpose_docs_1():
    assert transpose([[1, 3, 5], [2, 4, 6]]) == [[1, 2], [3, 4], [5, 6]]
    assert transpose([]) == None
    assert transpose([[]]) == None
    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
