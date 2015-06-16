from setuptools import setup

setup(name='courseradownload',
    version='0.2',
    description='Coursera Downloader',
    url='http://github.com/harshays/pyground',
    author='Harshay',
    author_email='harshay.rshah@gmail.com',
    license='MIT',
    packages=['courseradownload'],
    install_requires=['requests', 'beautifulsoup4'],
    entry_points = {
        'console_scripts': \
         ['courseradownload=courseradownload.courseradownload:help',
          'courseradownload.download=courseradownload.courseradownload:main']
    }
)