import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
# Don't import analytics-python module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'june','analytics'))
from version import VERSION

long_description = '''
June SDK is the simplest way to integrate analytics into your application.

Documentation and more details at https://www.june.so/docs/python
'''

install_requires = [
    "requests~=2.7",
    "monotonic~=1.5",
    "backoff~=1.10",
    "python-dateutil~=2.2"
]

tests_require = [
    "mock==2.0.0",
    "pylint==2.8.0",
    "flake8==3.7.9",
]

setup(
    name='juneso-analytics-python',
    version=VERSION,
    url='https://github.com/juneHQ/analytics-python',
    author='June',
    author_email='work@june.so',
    maintainer='June',
    maintainer_email='work@june.so',
    test_suite='analytics.test.all',
    packages=['june.analytics', 'analytics.test'],
    python_requires='>=3.6.0',
    license='MIT License',
    install_requires=install_requires,
    extras_require={
        'test': tests_require
    },
    description='The hassle-free way to integrate analytics into any python application.',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
