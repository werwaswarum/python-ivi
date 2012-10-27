

# http://docs.python.org/distutils/
# http://packages.python.org/distribute/
try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name = 'python-ivi',
    description = 'Python Interchangeable Virtual Instrument Library',
    version = '0.1',
    long_description = '''This package is a Python-based interpretation of the
Interchangeable Virtual Instrument standard, a software abstraction for
electronic test equipment that is remotely controllable.''',
    author = 'Alex Forencich',
    author_email = 'alex@alexforencich.com',
    url = 'http://alexforencich.com/wiki/en/python-ivi/start',
    download_url = 'http://github.com/alexforencich/python-ivi/tarball/master',
    keywords = 'IVI measurement instrument',
    license = 'MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Hardware',
        'Programming Language :: Python :: 3'
        ],
    packages = ['ivi', 'ivi.agilent', 'ivi.tektronix'],
    requires = ['numpy']
)

