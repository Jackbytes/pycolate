from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pycolate",
    version="0.0.21",
    author="Jack Harrington",
    author_email="jackjharrington@icloud.com",
    description="Generates site percolation data and illustrations.",
    packages=['pycolate'],
    install_requires=[
        'numpy',
        'scipy',
        'pillow'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: Physics']
)