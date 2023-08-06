from pathlib import Path
from setuptools import setup

MAIN_PACKAGE = 'heptapod_tests'
TESTS_PACKAGE = 'tests'
REQUIREMENTS_PATH = Path(__file__).parent / 'requirements.txt'

setup(
    name='heptapod-tests',
    version='0.9.0',
    author='octobus',
    author_email='contact@octobus.net',
    url='https://foss.heptapod.net/heptapod/heptapod-tests',
    long_description=Path('README.md').read_text(),
    long_description_content_type="text/markdown",
    description='Heptapod Functional Tests',
    keywords='hg mercurial git heptapod gitlab selenium REST GraphQL',
    packages=[MAIN_PACKAGE],
    license='GPL3+',
    install_requires=REQUIREMENTS_PATH.read_text().splitlines(),
)
