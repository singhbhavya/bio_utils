from setuptools import setup, find_packages

setup(
    name='bio_utils',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scanpy',
        'gseapy',
        'pandas',
        'matplotlib',
    ],
    author='Bhavya Singh',
    author_email='bhavya.singh@icahn.mssm.edu',
    description='Tools for for analyzing single-cell RNA-seq and spatial transcriptomic data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/singhbhavya/bio_utils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
