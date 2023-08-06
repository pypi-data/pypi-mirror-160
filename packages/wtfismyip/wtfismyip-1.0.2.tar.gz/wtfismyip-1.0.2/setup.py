from setuptools import setup

setup(
    name="wtfismyip",
    description='Get your fucking IP address',
    long_description='A simple script to get your IP address and its information on your terminal.',
    author='Jorge Alberto Díaz Orozco (Akiel)',
    author_email='diazorozcoj@gmail.com',
    version="1.0.2",
    scripts=["wtfismyip", ],
    install_requires=["requests", "rich", ]
)
