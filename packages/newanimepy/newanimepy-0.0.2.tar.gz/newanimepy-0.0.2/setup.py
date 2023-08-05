import setuptools, re
from setuptools import setup

with open('animepy/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.md', 'r', encoding="utf_8") as f:
    readme = f.read()

setup(
    name='newanimepy',
    version=version,
    author='Misaka0502',
    author_email='remisaka0502@gmail.com',
    description='An anime crawler',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/z20030818/NewAnimepy',
    packages= setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3.9"],
    install_requires=[
        "requests",
        "bs4"
    ]
)