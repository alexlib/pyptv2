"""Tests for the PyPTV2 CLI."""

import unittest
from unittest.mock import patch
import sys
import io
from pathlib import Path

from pyptv2.cli import cli


class TestCLI(unittest.TestCase):
    """Tests for the PyPTV2 CLI."""
    
    def setUp(self):
        """Set up test environment."""
        self.original_stdout = sys.stdout
        sys.stdout = io.StringIO()
    
    def tearDown(self):
        """Restore test environment."""
        sys.stdout = self.original_stdout
    
    @patch('sys.argv', ['pyptv2', '--version'])
    def test_version(self):
        """Test version command."""
        with patch('pyptv2.cli.cli') as mock_cli:
            from pyptv2.__main__ import main
            main()
            mock_cli.assert_not_called()
    
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_calibrate(self, mock_args):
        """Test calibrate command."""
        test_dir = Path.cwd()
        mock_args.return_value.command = 'calibrate'
        mock_args.return_value.path = str(test_dir)
        
        result = cli()
        
        output = sys.stdout.getvalue()
        self.assertIn("Running calibration for experiment", output)
        self.assertEqual(result, "CLI execution completed")
    
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_detect(self, mock_args):
        """Test detect command."""
        test_dir = Path.cwd()
        mock_args.return_value.command = 'detect'
        mock_args.return_value.path = str(test_dir)
        
        result = cli()
        
        output = sys.stdout.getvalue()
        self.assertIn("Running particle detection for experiment", output)
        self.assertEqual(result, "CLI execution completed")
    
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_track(self, mock_args):
        """Test track command."""
        test_dir = Path.cwd()
        mock_args.return_value.command = 'track'
        mock_args.return_value.path = str(test_dir)
        
        result = cli()
        
        output = sys.stdout.getvalue()
        self.assertIn("Running tracking for experiment", output)
        self.assertEqual(result, "CLI execution completed")


if __name__ == '__main__':
    unittest.main()