import configparser

import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# following block reads deps from Pipfile nearby
# used as temporary fix to the unperfection of the world :) https://github.com/pypa/pipenv/issues/1263

install_requires = []
config = configparser.ConfigParser()
config.read('Pipfile')

if 'packages' not in config:
    raise Exception(
        'Unable to complete install_requires list. '
        'No packages section in Pipfile nearby.'
    )

for package in config['packages']:
    install_requires.append(package)


setuptools.setup(
    name='trade-utils',
    version='1.0.1',
    author='darnes',
    author_email='darnesmeister@gmail.com',
    license='MIT',
    description=(
        'Algo trading utils package. '
        'Zero test-coverage so use on your own risk.'
    ),

    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/darnes/algo',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    include_package_data=True,
    install_requires=install_requires
)
