from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='torch_clip',
    version='0.0.6',
    packages=['torch_clip'],
    url='',
    license='MIT',
    author='Nikolay',
    author_email='kutuzov.nv@phystech.edu',
    description='torch-clip a library to improve optimization methods by clipping off heavy-tailed gradient. '
                'This makes it possible to increase the accuracy and speed of convergence during the training '
                'of neural networks on a specific number of tasks.',
    long_description=long_description,
    keywords=['python', 'torch', 'clipping'],
    long_description_content_type="text/markdown",
)
