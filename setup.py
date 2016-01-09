from setuptools import setup

# PyPI only supports nicely-formatted README files in reStructuredText.
# Newsapps seems to prefer Markdown.  Use a version of the pattern from
# https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
# to convert the Markdown README to rst if the pypandoc package is
# present.
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError):
    long_description = open('README.md').read()

# Load the version from the version module
exec(open('cps_schools/version.py').read())

setup(
    name='cps_schools',
    version=__version__,
    py_modules=['cps_schools'],
    install_requires=[
        # TODO: Separate out data loading dependencies
        'dataset',
        'psycopg2',
        'invoke',
        'requests',
        'xlrd',
        'unicodecsv',
    ],
    tests_require=[
        'nose',
    ],
    test_suite='nose.collector',
)
