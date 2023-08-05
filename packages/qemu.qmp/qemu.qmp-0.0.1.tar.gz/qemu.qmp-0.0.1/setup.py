#!/usr/bin/env python3
"""
QEMU QMP library installer script
Copyright (c) 2020-2021 John Snow for Red Hat, Inc.
"""

import setuptools
from setuptools.command import bdist_egg
import sys
import pkg_resources


try:
    import setuptools_scm
    _HAVE_SCM = True
except ModuleNotFoundError:
    _HAVE_SCM = False


class bdist_egg_guard(bdist_egg.bdist_egg):
    """
    Protect against bdist_egg from being executed

    This prevents calling 'setup.py install' directly, as the 'install'
    CLI option will invoke the deprecated bdist_egg hook. "pip install"
    calls the more modern bdist_wheel hook, which is what we want.
    """
    def run(self):
        sys.exit(
            'Installation directly via setup.py is not supported.\n'
            'Please use `pip install .` instead.'
        )


def main():
    """
    QEMU tooling installer
    """

    # https://medium.com/@daveshawley/safely-using-setup-cfg-for-metadata-1babbe54c108
    pkg_resources.require('setuptools>=39.2')

    kwargs = {
        'cmdclass': {'bdist_egg': bdist_egg_guard},
        'use_scm_version': {'fallback_version': '0.0.0'}
    }

    setuptools.setup(**kwargs)


if __name__ == '__main__':
    main()
