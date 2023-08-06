from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]

setup(
    name='capturebaudrate',
    version='0.0.3',
    description='A very basic capture',
    long_description=open('README').read() + '\n\n' + open('CHANGELOG').read(),
    url='',
    author='Ao Zhang',
    author_email='aozhang2022@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)