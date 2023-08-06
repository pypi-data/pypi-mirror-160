from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='memoryuse',
    version='0.0.1',
    description='memory tracker displayer',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Ivan Gonzalez Schulten',
    author_email='iagonzalez7@uc.cl',
    license='MIT',
    classifiers=classifiers,
    keywords='memory',
    packages=find_packages(),
    install_requires=[]
)