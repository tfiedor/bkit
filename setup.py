from setuptools import setup

setup(
    name='bkit',
    version='0.1',
    py_modules=['bkit'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        bkit=bkit:cli
    ''',
)