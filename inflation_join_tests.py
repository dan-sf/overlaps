import mock
import unittest
import tempfile
import sys
import inflation_join
import os

class TestInflationJoin(unittest.TestCase):
    def test_join_data(self):
        tmp_stream = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_stream.name, 'w') as f:
            f.write('one\n')

        try:
            with mock.patch('inflation_join.print_list') as mock_print_list:
                inflation_join.join_data(tmp_stream, 0, {'one': [['1']]})
                mock_print_list.assert_called_with(['one', '1'])
        finally:
            os.remove(tmp_stream.name)

    def test_join_data_printall(self):
        tmp_stream = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_stream.name, 'w') as f:
            f.write('two\n')

        try:
            with mock.patch('inflation_join.print_list') as mock_print_list:
                inflation_join.join_data(tmp_stream, 0, {'one': [['1']]}, printall="PRINT")
                mock_print_list.assert_called_with(['two', 'PRINT'])
        finally:
            os.remove(tmp_stream.name)

    def test_print_list(self):
        row = ['one', 'two', 'three']
        with mock.patch('sys.stdout') as mock_stdout:
            inflation_join.print_list(row)
            mock_stdout.write.assert_called_with('one\ttwo\tthree\n')

    def test_remove_join_key(self):
        row = ['one', 'two', 'three']
        actual = inflation_join.remove_join_key(row, 'two')
        expected = ['one', 'three']
        self.assertEqual(actual, expected)

    def test_create_join(self):
        tmp_join = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_join.name, 'w') as f:
            f.write('one\t1\n')
            f.write('two\t2\n')
            f.write('three\t3\n')

        actual = inflation_join.create_join(tmp_join.name, 0)
        expected = { 'one': [['1']], 'two': [['2']], 'three': [['3']] }

        self.assertEqual(actual, expected)
        os.remove(tmp_join.name)

if __name__ == '__main__':
    unittest.main()

