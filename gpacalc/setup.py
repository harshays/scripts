from setuptools import setup

setup(name='gpacalc',
    version='0.2',
    description='gpa calculator',
    url='http://github.com/harshays/scripts',
    author='Harshay',
    author_email='harshay.rshah@gmail.com',
    license='MIT',
    packages=['gpacalc'],
    install_requires=[],
    entry_points = {
        'console_scripts': ['gpacalc = gpacalc.gpacalc:main']
    }
)