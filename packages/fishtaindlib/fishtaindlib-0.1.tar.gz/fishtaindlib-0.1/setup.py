from setuptools import setup,find_packages

import os



VERSION = '0.1'
DESCRIPTION = 'A Python Library by Finnovesh for Technical Indicators commonly used for Trading in Financial markets'
LONG_DESCRIPTION = 'A Python Library by Finnovesh for Technical Indicators commonly used for Trading in Financial markets'

# Setting up
setup(
    name="fishtaindlib",
    version=VERSION,
    author="Finnovesh (Finnovesh Incorporation)",
    author_email="<finnovesh@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=['fishtaindlib'],
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