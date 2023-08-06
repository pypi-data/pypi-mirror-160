from gettext import install
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='firstsdk',
    version='0.0.2',
    description='A simple sdk that consumes an api',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Elias Berumen de Haro',
    author_email='ebdh_9011@hotmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='sdk',
    packages=find_packages(),
    install_requires=['requests']
)