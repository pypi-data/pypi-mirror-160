from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='geniusmlapi',
    version='0.0.1',
    url='https://github.com/fagnercandido/GeniusMLAPI',
    license='MIT License',
    author='Fagner Candido',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='fsouzacandido@gmail.com',
    keywords='Pacote',
    description=u'Pacote PyPI para Genius',
    packages=['geniusmlapi'],
    install_requires=['numpy', 'requests', 'bs4', 'string', 'pandas'],)