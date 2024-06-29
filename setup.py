from setuptools import setup, find_packages

setup(
    name='FootyStatsPy',
    version='0.1.0',
    description='A Python library for football data scraping and visualization',
    author='Jesús Antolín Felipe',
    author_email='jaf.attd@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
        'mplsoccer',
        'matplotlib',
        'Pillow',
        'lxml'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

