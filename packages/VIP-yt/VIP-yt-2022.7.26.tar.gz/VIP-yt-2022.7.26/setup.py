#!/usr/bin/env python3

import os.path
import subprocess
import sys
import warnings

try:
    from setuptools import Command, find_packages, setup
    setuptools_available = True
except ImportError:
    from distutils.core import Command, setup
    setuptools_available = False


def read(fname):
    with open(fname, encoding='utf-8') as f:
        return f.read()


# Get the version from VIP_yt/version.py without importing the package
def read_version(fname):
    exec(compile(read(fname), fname, 'exec'))
    return locals()['__version__']


VERSION = read_version('VIP_yt/version.py')

DESCRIPTION = 'A youtube-dl fork with additional features and patches'

LONG_DESCRIPTION = '\n\n'.join((
    'Official repository: <https://github.com/VIP-yt/VIP-yt>',
    '**PS**: Some links in this document will not work since this is a copy of the README.md from Github',
    read('README.md')))

REQUIREMENTS = read('requirements.txt').splitlines()


def packages():
    if setuptools_available:
        return find_packages(exclude=('youtube_dl', 'youtube_dlc', 'test', 'ytdlp_plugins'))

    return [
        'VIP_yt', 'VIP_yt.extractor', 'VIP_yt.downloader', 'VIP_yt.postprocessor', 'VIP_yt.compat',
        'VIP_yt.extractor.anvato_token_generator',
    ]


def py2exe_params():
    import py2exe  # noqa: F401

    warnings.warn(
        'py2exe builds do not support pycryptodomex and needs VC++14 to run. '
        'The recommended way is to use "pyinst.py" to build using pyinstaller')

    return {
        'console': [{
            'script': './VIP_yt/__main__.py',
            'dest_base': 'VIP-yt',
            'version': VERSION,
            'description': DESCRIPTION,
            'comments': LONG_DESCRIPTION.split('\n')[0],
            'product_name': 'VIP-yt',
            'product_version': VERSION,
            'icon_resources': [(1, 'devscripts/logo.ico')],
        }],
        'options': {
            'py2exe': {
                'bundle_files': 0,
                'compressed': 1,
                'optimize': 2,
                'dist_dir': './dist',
                'excludes': ['Crypto', 'Cryptodome'],  # py2exe cannot import Crypto
                'dll_excludes': ['w9xpopen.exe', 'crypt32.dll'],
                # Modules that are only imported dynamically must be added here
                'includes': ['VIP_yt.compat._legacy'],
            }
        },
        'zipfile': None
    }


def build_params():
    files_spec = [
        ('share/bash-completion/completions', ['completions/bash/VIP-yt']),
        ('share/zsh/site-functions', ['completions/zsh/_VIP-yt']),
        ('share/fish/vendor_completions.d', ['completions/fish/VIP-yt.fish']),
        ('share/doc/VIP_yt', ['README.txt']),
        ('share/man/man1', ['VIP-yt.1'])
    ]
    data_files = []
    for dirname, files in files_spec:
        resfiles = []
        for fn in files:
            if not os.path.exists(fn):
                warnings.warn(f'Skipping file {fn} since it is not present. Try running " make pypi-files " first')
            else:
                resfiles.append(fn)
        data_files.append((dirname, resfiles))

    params = {'data_files': data_files}

    if setuptools_available:
        params['entry_points'] = {'console_scripts': ['VIP-yt = VIP_yt:main']}
    else:
        params['scripts'] = ['VIP-yt']
    return params


class build_lazy_extractors(Command):
    description = 'Build the extractor lazy loading module'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if self.dry_run:
            print('Skipping build of lazy extractors in dry run mode')
            return
        subprocess.run([sys.executable, 'devscripts/make_lazy_extractors.py', 'VIP_yt/extractor/lazy_extractors.py'])


params = py2exe_params() if sys.argv[1:2] == ['py2exe'] else build_params()
setup(
    name='VIP-yt',
    version=VERSION,
    maintainer='Abdo-Asil',
    maintainer_email='pukkandan.ytdlp@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/VIP-yt/VIP-yt',
    packages=packages(),
    install_requires=REQUIREMENTS,
    python_requires='>=3.7',
    project_urls={
        'Documentation': 'https://github.com/VIP-yt/VIP-yt#readme',
        'Source': 'https://github.com/VIP-yt/VIP-yt',
        'Tracker': 'https://github.com/VIP-yt/VIP-yt/issues',
        'Funding': 'https://github.com/VIP-yt/VIP-yt/blob/master/Collaborators.md#collaborators',
    },
    classifiers=[
        'Topic :: Multimedia :: Video',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: Public Domain',
        'Operating System :: OS Independent',
    ],
    cmdclass={'build_lazy_extractors': build_lazy_extractors},
    **params
)
