from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='openfunction',
    version='0.0.1',
    description='Open function for ports',
    long_description=open('README').read() + '\n\n' + open('CHANGELOG').read(),
    url='',
    author='Ao Zhang',
    author_email='aozhang2022@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='open',
    packages=find_packages(),
    install_requires=['']
)