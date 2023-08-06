import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='api_easiedata', # Replace with your own username
    version='0.1.4',
    author='The easiedata team',
    author_email='barsand@easiedata.com',
    description='Module to facilitate the interaction with easiedata\'s HTTP interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/easiedata/api_easiedata',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>= 3.6',
    install_requires=[
        'requests==2.25.1',
        'pandas==1.1.5'
    ]
)
