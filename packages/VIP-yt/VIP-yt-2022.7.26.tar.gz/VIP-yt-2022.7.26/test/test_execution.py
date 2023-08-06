#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import contextlib
import subprocess

from VIP_yt.utils import encodeArgument

rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


try:
    _DEV_NULL = subprocess.DEVNULL
except AttributeError:
    _DEV_NULL = open(os.devnull, 'wb')


class TestExecution(unittest.TestCase):
    def test_import(self):
        subprocess.check_call([sys.executable, '-c', 'import VIP_yt'], cwd=rootDir)

    def test_module_exec(self):
        subprocess.check_call([sys.executable, '-m', 'VIP_yt', '--ignore-config', '--version'], cwd=rootDir, stdout=_DEV_NULL)

    def test_main_exec(self):
        subprocess.check_call([sys.executable, 'VIP_yt/__main__.py', '--ignore-config', '--version'], cwd=rootDir, stdout=_DEV_NULL)

    def test_cmdline_umlauts(self):
        p = subprocess.Popen(
            [sys.executable, 'VIP_yt/__main__.py', '--ignore-config', encodeArgument('ä'), '--version'],
            cwd=rootDir, stdout=_DEV_NULL, stderr=subprocess.PIPE)
        _, stderr = p.communicate()
        self.assertFalse(stderr)

    def test_lazy_extractors(self):
        try:
            subprocess.check_call([sys.executable, 'devscripts/make_lazy_extractors.py', 'VIP_yt/extractor/lazy_extractors.py'], cwd=rootDir, stdout=_DEV_NULL)
            subprocess.check_call([sys.executable, 'test/test_all_urls.py'], cwd=rootDir, stdout=_DEV_NULL)
        finally:
            with contextlib.suppress(OSError):
                os.remove('VIP_yt/extractor/lazy_extractors.py')


if __name__ == '__main__':
    unittest.main()
