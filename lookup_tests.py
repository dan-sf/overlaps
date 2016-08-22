import mock
import unittest
import tempfile
import sys
import lookup
import os

class TestLookup(unittest.TestCase):
    def test_print_data(self):
        record = ['one', 'two', 'three']
        with mock.patch('sys.stdout') as mock_stdout:
            lookup.print_data(record)
            mock_stdout.write.assert_called_with('one\ttwo\tthree\n')

    def test_lookup_set(self):
        test_outfile = tempfile.NamedTemporaryFile()
        test_outfile.write('one\n')
        test_outfile.flush()
        actual = lookup.lookup_set(test_outfile.name)
        expected = { 'one' }
        self.assertEqual(actual, expected)

    def test_filter_data_include(self):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_file.name, 'w') as f:
            f.write('one\n')

        args = mock.MagicMock()
        args.file = tmp_file.name
        args.remove = False
        args.column = 0

        tmp_stream = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_stream.name, 'w') as f:
            f.write('one\n')
            f.write('two\n')

        try:
            with mock.patch('lookup.print_data') as mock_print_data:
                lookup.filter_data(tmp_stream, args)
                mock_print_data.assert_called_with(['one'])
        finally:
            os.remove(args.file)
            os.remove(tmp_stream.name)

    def test_filter_data_remove(self):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_file.name, 'w') as f:
            f.write('one\n')

        args = mock.MagicMock()
        args.file = tmp_file.name
        args.remove = True
        args.column = 0

        tmp_stream = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp_stream.name, 'w') as f:
            f.write('one\n')
            f.write('two\n')

        try:
            with mock.patch('lookup.print_data') as mock_print_data:
                lookup.filter_data(tmp_stream, args)
                mock_print_data.assert_called_with(['two'])
        finally:
            os.remove(args.file)
            os.remove(tmp_stream.name)

if __name__ == '__main__':
    unittest.main()

