from pytest import raises
from technical_test import (DataCapture, DataStats, OutOfRangeException, InvalidTypeException,
                            NegativeValueException, NoValuesException)


class TestDataCaptureAdd:

    def test_add_out_limit_values_raise_out_of_range_exception(self):
        capture = DataCapture()
        capture.add(1)
        capture.add(200)

        with raises(OutOfRangeException):
            capture.add(0)

        with raises(OutOfRangeException):
            capture.add(1001)

    def test_add_float_value_raise_invalid_type_exception(self):
        capture = DataCapture()

        with raises(InvalidTypeException):
            capture.add(4.3)

        capture.add(14)
        capture.add(872)

        with raises(InvalidTypeException):
            capture.add(82.3)

    def test_add_negative_values_raise_negative_value_exception(self):
        capture = DataCapture()

        with raises(NegativeValueException):
            capture.add(-3)

        capture.add(5)
        capture.add(716)

        with raises(NegativeValueException):
            capture.add(-8)

    def test_add_valid_limits(self):
        capture = DataCapture()
        capture.add(1)
        capture.add(1000)

        assert capture.numbers_count.get(1) == 1
        assert capture.numbers_count.get(1000) == 1

    def test_add_multiple_valid_values(self):
        capture = DataCapture()
        capture.add(14)
        capture.add(87)
        capture.add(62)
        capture.add(982)
        capture.add(562)
        capture.add(116)
        capture.add(3)

        assert capture.numbers_count.get(14) == 1
        assert capture.numbers_count.get(87) == 1
        assert capture.numbers_count.get(62) == 1
        assert capture.numbers_count.get(982) == 1
        assert capture.numbers_count.get(562) == 1
        assert capture.numbers_count.get(116) == 1
        assert capture.numbers_count.get(3) == 1

    def test_add_multiple_valid_and_duplicated_values(self):
        capture = DataCapture()
        capture.add(14)
        capture.add(87)
        capture.add(62)
        capture.add(982)
        capture.add(62)
        capture.add(62)
        capture.add(14)

        assert capture.numbers_count.get(14) == 2
        assert capture.numbers_count.get(87) == 1
        assert capture.numbers_count.get(62) == 3
        assert capture.numbers_count.get(982) == 1


class TestDataCaptureBuildStats:

    def test_build_stats_without_values_raise_no_values_exception(self):
        capture = DataCapture()

        with raises(NoValuesException):
            capture.build_stats()

    def test_build_stats_return_data_capture_instance(self):
        capture = DataCapture()
        capture.add(15)
        assert isinstance(capture.build_stats(), DataStats)

    def test_build_stats_single_valid_values(self):
        capture = DataCapture()
        capture.add(10)
        capture.add(45)
        capture.add(997)
        stats = capture.build_stats()

        assert stats.numbers_stats.get(9) == 0
        assert stats.numbers_stats.get(10) == 1
        assert stats.numbers_stats.get(11) == 1
        assert stats.numbers_stats.get(44) == 1
        assert stats.numbers_stats.get(45) == 2
        assert stats.numbers_stats.get(46) == 2
        assert stats.numbers_stats.get(996) == 2
        assert stats.numbers_stats.get(997) == 3
        assert stats.numbers_stats.get(998) == 3

    def test_build_stats_duplicated_valid_values(self):
        capture = DataCapture()
        capture.add(56)
        capture.add(872)
        capture.add(998)
        capture.add(872)
        capture.add(872)
        capture.add(1000)
        stats = capture.build_stats()

        assert stats.numbers_stats.get(55) == 0
        assert stats.numbers_stats.get(56) == 1
        assert stats.numbers_stats.get(57) == 1
        assert stats.numbers_stats.get(871) == 1
        assert stats.numbers_stats.get(872) == 4
        assert stats.numbers_stats.get(873) == 4
        assert stats.numbers_stats.get(997) == 4
        assert stats.numbers_stats.get(998) == 5
        assert stats.numbers_stats.get(999) == 5
        assert stats.numbers_stats.get(1000) == 6


class TestDataCaptureLess:

    def test_less_negative_number_raise_negative_value_exception(self):
        capture = DataCapture()
        capture.add(47)
        stats = capture.build_stats()

        with raises(NegativeValueException):
            stats.less(-14)

    def test_less_float_number_raise_invalid_type_exception(self):
        capture = DataCapture()
        capture.add(47)
        stats = capture.build_stats()

        with raises(InvalidTypeException):
            stats.less(178.2)
            
    def test_less_out_of_range_number_raise_out_of_range_exception(self):
        capture = DataCapture()
        capture.add(47)
        stats = capture.build_stats()

        with raises(OutOfRangeException):
            stats.less(1001)
            
        with raises(OutOfRangeException):
            stats.less(0)

    def test_less_single_correct_values(self):
        capture = DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(70)
        capture.add(4)
        capture.add(6)
        stats = capture.build_stats()

        assert stats.less(3) == 0
        assert stats.less(4) == 1
        assert stats.less(5) == 2
        assert stats.less(6) == 2
        assert stats.less(7) == 3
        assert stats.less(9) == 3
        assert stats.less(10) == 4
        assert stats.less(70) == 4
        assert stats.less(71) == 5
        assert stats.less(1000) == 5

    def test_less_duplicated_correct_values(self):
        capture = DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(70)
        capture.add(70)
        capture.add(70)
        capture.add(4)
        capture.add(4)
        capture.add(4)
        capture.add(4)
        capture.add(9)
        capture.add(6)
        capture.add(6)
        stats = capture.build_stats()

        assert stats.less(3) == 0
        assert stats.less(4) == 1
        assert stats.less(5) == 5
        assert stats.less(6) == 5
        assert stats.less(7) == 7
        assert stats.less(9) == 7
        assert stats.less(10) == 9
        assert stats.less(70) == 9
        assert stats.less(71) == 12
        assert stats.less(1000) == 12

    def test_less_correct_values_with_limit_values(self):
        capture = DataCapture()
        capture.add(1000)
        capture.add(3)
        capture.add(9)
        capture.add(70)
        capture.add(70)
        capture.add(70)
        capture.add(4)
        capture.add(1)
        capture.add(4)
        capture.add(4)
        capture.add(4)
        capture.add(9)
        capture.add(6)
        capture.add(6)
        capture.add(1000)
        stats = capture.build_stats()

        assert stats.less(1) == 0
        assert stats.less(2) == 1
        assert stats.less(3) == 1
        assert stats.less(4) == 2
        assert stats.less(5) == 6
        assert stats.less(6) == 6
        assert stats.less(7) == 8
        assert stats.less(9) == 8
        assert stats.less(10) == 10
        assert stats.less(70) == 10
        assert stats.less(71) == 13
        assert stats.less(1000) == 13


class TestDataCaptureGreater:

    def test_greater_negative_number_raise_negative_value_exception(self):
        capture = DataCapture()
        capture.add(47)
        stats = capture.build_stats()

        with raises(NegativeValueException):
            stats.greater(-8273)

    def test_greater_float_number_raise_invalid_type_exception(self):
        capture = DataCapture()
        capture.add(47)
        stats = capture.build_stats()

        with raises(InvalidTypeException):
            stats.greater(1.1)
            
    def test_greater_out_of_range_number_raise_out_of_range_exception(self):
        capture = DataCapture()
        capture.add(47)
        stats = capture.build_stats()

        with raises(OutOfRangeException):
            stats.greater(1001)
            
        with raises(OutOfRangeException):
            stats.greater(0)

    def test_greater_single_correct_values(self):
        capture = DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(70)
        capture.add(4)
        capture.add(6)
        stats = capture.build_stats()

        assert stats.greater(2) == 5
        assert stats.greater(3) == 4
        assert stats.greater(4) == 3
        assert stats.greater(5) == 3
        assert stats.greater(6) == 2
        assert stats.greater(7) == 2
        assert stats.greater(9) == 1
        assert stats.greater(10) == 1
        assert stats.greater(70) == 0
        assert stats.greater(71) == 0

    def test_greater_duplicated_correct_values(self):
        capture = DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(70)
        capture.add(70)
        capture.add(70)
        capture.add(4)
        capture.add(4)
        capture.add(4)
        capture.add(4)
        capture.add(9)
        capture.add(6)
        capture.add(6)
        stats = capture.build_stats()

        assert stats.greater(2) == 12
        assert stats.greater(3) == 11
        assert stats.greater(4) == 7
        assert stats.greater(5) == 7
        assert stats.greater(6) == 5
        assert stats.greater(7) == 5
        assert stats.greater(9) == 3
        assert stats.greater(10) == 3
        assert stats.greater(70) == 0
        assert stats.greater(71) == 0

    def test_greater_correct_values_with_limit_values(self):
        capture = DataCapture()
        capture.add(1000)
        capture.add(3)
        capture.add(9)
        capture.add(70)
        capture.add(70)
        capture.add(70)
        capture.add(4)
        capture.add(1)
        capture.add(4)
        capture.add(4)
        capture.add(4)
        capture.add(9)
        capture.add(6)
        capture.add(6)
        capture.add(1000)
        stats = capture.build_stats()

        assert stats.greater(1) == 14
        assert stats.greater(2) == 14
        assert stats.greater(3) == 13
        assert stats.greater(4) == 9
        assert stats.greater(5) == 9
        assert stats.greater(6) == 7
        assert stats.greater(7) == 7
        assert stats.greater(9) == 5
        assert stats.greater(10) == 5
        assert stats.greater(70) == 2
        assert stats.greater(71) == 2
        assert stats.greater(1000) == 0


class TestDataCaptureBetween:

    def test_between_negative_number_raise_negative_value_exception(self):
        capture = DataCapture()
        capture.add(47)
        stats = capture.build_stats()

        with raises(NegativeValueException):
            stats.between(-10, 15)

        with raises(NegativeValueException):
            stats.between(77, -33)

        with raises(NegativeValueException):
            stats.between(-1, -50)

    def test_between_float_number_raise_invalid_type_exception(self):
        capture = DataCapture()
        capture.add(47)
        stats = capture.build_stats()

        with raises(InvalidTypeException):
            stats.between(1.50, 15)

        with raises(InvalidTypeException):
            stats.between(70, 105.6)

        with raises(InvalidTypeException):
            stats.between(1.50, 198.2)
            
    def test_between_out_of_range_number_raise_out_of_range_exception(self):
        capture = DataCapture()
        capture.add(47)
        stats = capture.build_stats()

        with raises(OutOfRangeException):
            stats.greater(10, 1001)
            
        with raises(OutOfRangeException):
            stats.greater(0, 70)
            
        with raises(OutOfRangeException):
            stats.greater(0,1001)

    def test_between_single_correct_values(self):
        capture = DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(70)
        capture.add(4)
        capture.add(6)
        stats = capture.build_stats()

        assert stats.between(1, 4) == 2
        assert stats.between(4, 1) == 2
        assert stats.between(5, 10) == 2
        assert stats.between(9, 71) == 2
        assert stats.between(70, 1000) == 1
        assert stats.between(1, 1000) == 5

    def test_between_duplicated_correct_values(self):
        capture = DataCapture()
        capture.add(3)
        capture.add(9)
        capture.add(70)
        capture.add(70)
        capture.add(70)
        capture.add(4)
        capture.add(4)
        capture.add(4)
        capture.add(4)
        capture.add(9)
        capture.add(6)
        capture.add(6)
        stats = capture.build_stats()

        assert stats.between(1, 4) == 5
        assert stats.between(5, 10) == 4
        assert stats.between(9, 71) == 5
        assert stats.between(70, 1000) == 3
        assert stats.between(1, 1000) == 12

    def test_between_correct_values_with_limit_values(self):
        capture = DataCapture()
        capture.add(1000)
        capture.add(3)
        capture.add(9)
        capture.add(70)
        capture.add(70)
        capture.add(70)
        capture.add(4)
        capture.add(1)
        capture.add(4)
        capture.add(4)
        capture.add(4)
        capture.add(9)
        capture.add(6)
        capture.add(6)
        capture.add(1000)
        stats = capture.build_stats()

        assert stats.between(1, 4) == 6
        assert stats.between(5, 10) == 4
        assert stats.between(9, 71) == 5
        assert stats.between(70, 1000) == 5
        assert stats.between(1, 1000) == 15
