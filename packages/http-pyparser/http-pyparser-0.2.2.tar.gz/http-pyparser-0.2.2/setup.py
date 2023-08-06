from setuptools import setup
from http_pyparser import __version__

with open('README.md', 'r') as reader:
    long_description = reader.read()

setup(
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    name='http-pyparser',
    description='Parse HTTP messages simply and quickly with Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=__version__,
    packages=['http_pyparser'],
    keywords=['http', 'parser', 'python', 'request'],
    license='Apache 2.0',
    platforms=['any'],
    url='https://github.com/jaedsonpys/http-pyparser',
    python_requires='>= 3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)