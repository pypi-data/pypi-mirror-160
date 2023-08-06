from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='FuncsForSPO',
    version='0.0.3.10',
    url='https://github.com/githubpaycon/FuncsForSPO',
    license='MIT License',
    author='Gabriel Lopes de Souza',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='githubpaycon@gmail.com',
    keywords='Funções Para Melhorar Desenvolvimento de Robôs com Selenium',
    description=u'Funções Para Melhorar Desenvolvimento de Robôs com Selenium',
    packages=['FuncsForSPO'],
    install_requires=['selenium', 'openpyxl', 'psutil', 'webdriver-manager', 'fake_useragent', 'requests'],
    )