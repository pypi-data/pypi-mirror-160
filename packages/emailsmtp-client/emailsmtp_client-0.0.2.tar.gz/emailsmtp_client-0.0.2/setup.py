from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.02'
DESCRIPTION = 'yess'
LONG_DESCRIPTION = 'yesssss'

# Setting up
setup(
    name="emailsmtp_client",
    version=VERSION,
    author="champu bai dan",
    author_email="temporarywebhosting@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    py_modules=["emailsmtp_client"],
    package_dir={'': 'src'},
    packages=find_packages(),
    install_requires=['mysql.connector'],
    keywords=['python', 'hacking', 'cybersecurity', 'hacking tools', 'security testing', 'hacker'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
