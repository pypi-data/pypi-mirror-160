import os
import re
from setuptools import find_packages, setup

with open('README.md', encoding='cp850') as f:
    long_description = f.read()

HERE = os.path.dirname(os.path.abspath(__file__))
def get_version():
    filename = os.path.join(HERE, 'Gitlog', '__init__.py')
    with open(filename) as ver:
        contents = ver.read()
    pattern = r"^__version__ = '(.*?)'$"
    return re.search(pattern, contents, re.MULTILINE).group(1)

setup(
    name='Gitlog',
    packages=find_packages('.', exclude=['tests', 'tests.*']),

    version=get_version(),
    description='Gitlog is a python library to work with @github logs. 📈',
    author='Amir Shamsi',
    url='https://github.com/Amir-Shamsi/Gitlog',

    license='MIT',
    author_email='amirshamsi.github@gmail.com',

    github='https://github.com/Amir-Shamsi',
    linkedin='https://linkedin.com/in/amir-shamsi',

    install_requires=[],
    download_url='https://github.com/Amir-Shamsi/Gitlog/archive/refs/tags/' + get_version() + '.tar.gz',

    requires=['requests', 'simplejson'],
    keywords=['Github', 'logs', 'api', 'git', 'followers', 'followings', 'profile'],
    setup_requires=['pytest-runner==6.0.0'],
    tests_require=['pytest==7.1.2'],
    test_suite='tests',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
