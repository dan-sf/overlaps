import mock
import unittest
import tempfile
import sys
import replace
import os

class TestReplace(unittest.TestCase):
    def test_print_data(self):
        record = ['one', 'two', 'three']
        with mock.patch('sys.stdout') as mock_stdout:
            replace.print_data(record)
            mock_stdout.write.assert_called_with('one\ttwo\tthree\n')

    def test_create_lookup(self):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_file.name, 'w') as f:
            f.write('one\t1\n')
            f.write('two\t2\n')
            f.write('three\t3\n')
        actual = replace.create_lookup(tmp_file.name)
        expected = { 'one': '1', 'two': '2', 'three': '3' }
        self.assertEqual(actual, expected)
        os.remove(tmp_file.name)

    def test_join_data_append(self):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_file.name, 'w') as f:
            f.write('one\t1\n')
            f.write('two\t2\n')
            f.write('three\t3\n')

        args = mock.MagicMock()
        args.file = tmp_file.name
        args.column = 0
        args.printall = None
        args.replace = False

        tmp_stream = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_stream.name, 'w') as f:
            f.write('three\n')
            f.write('four\n')

        try:
            with mock.patch('replace.print_data') as mock_print_data:
                replace.join_data(tmp_stream, args)
                mock_print_data.assert_called_with(['three','3'])
        finally:
            os.remove(args.file)
            os.remove(tmp_stream.name)

    def test_join_data_replace(self):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_file.name, 'w') as f:
            f.write('one\t1\n')
            f.write('two\t2\n')
            f.write('three\t3\n')

        args = mock.MagicMock()
        args.file = tmp_file.name
        args.column = 0
        args.printall = None
        args.replace = True

        tmp_stream = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_stream.name, 'w') as f:
            f.write('three\n')
            f.write('four\n')

        try:
            with mock.patch('replace.print_data') as mock_print_data:
                replace.join_data(tmp_stream, args)
                mock_print_data.assert_called_with(['3'])
        finally:
            os.remove(args.file)
            os.remove(tmp_stream.name)

    def test_join_data_printall(self):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_file.name, 'w') as f:
            f.write('one\t1\n')
            f.write('two\t2\n')
            f.write('three\t3\n')

        args = mock.MagicMock()
        args.file = tmp_file.name
        args.column = 0
        args.printall = 'PRINT'
        args.replace = False

        tmp_stream = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_stream.name, 'w') as f:
            f.write('four\n')

        try:
            with mock.patch('replace.print_data') as mock_print_data:
                replace.join_data(tmp_stream, args)
                mock_print_data.assert_called_with(['four','PRINT'])
        finally:
            os.remove(args.file)
            os.remove(tmp_stream.name)

if __name__ == '__main__':
    unittest.main()

