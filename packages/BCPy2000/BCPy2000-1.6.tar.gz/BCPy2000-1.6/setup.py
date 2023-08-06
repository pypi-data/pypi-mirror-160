from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()
setup(
    name='BCPy2000',
    version='1.6',
    description="A reimplementation of BCI2000 using Python", 
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url="https://github.com/neurotechcenter/BCpy2000",  
    license='GNU',
    author="Nicholas Luczak",
    author_email='luczak@neurotechcenter.org',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        # Pick your license as you wish
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires=">=3.6, <4",
    keywords="brain-computer interface, PsychoPy, experiment design, experiment control, science, neuroscience",
    install_requires=[
          'PsychoPy==2021.1.0', 'IPython==7.20.0', 'numpy==1.20.1',
      ],
    
)