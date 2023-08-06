from setuptools import setup,find_packages

import os



VERSION = '0.2'
DESCRIPTION = 'A Python Library of indicators (based on backtrader) commonly used in technical analysis while Trading in Financial markets.'
LONG_DESCRIPTION = 'A Python Library of indicators (based on backtrader) commonly used in technical analysis while Trading in Financial markets. This librabry is maintained by Saksham ( Platform supported by Finnovesh ) '

# Setting up
setup(
    name="saksham-bt-ind",
    version=VERSION,
    author="SAKSHAM (Platform powered by Finnovesh Incorporation)",
    author_email="<finnovesh@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=['saksham_bt_ind'],
    install_requires=['backtrader'],
    keywords=['python', 'keygennerator', 'keygen', 'password'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)