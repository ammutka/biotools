#!/usr/bin/env python

from distutils.core import setup

setup(name="biotools",
      version='1.1.5',
      description="A bunch of bioinformatics utilities.",
      long_description="""Accompanies Bart, Rebecca, *et al.* High-throughput genomic sequencing of Cassava Bacterial Blight strains identifies conserved effectors to target for durable resistance. *PNAS Plus*.

Currently depends on `clustalw <ftp://ftp.ebi.ac.uk/pub/software/clustalw2/2.1/>`_ and `BLAST <ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/>`_.""",
      author="Andrew Kassen",
      maintainer="Andrew Kassen",
      author_email="atkassen@gmail.com",
      maintainer_email="atkassen@gmail.com",
      url="https://github.com/sonwell/biotools",
      requires=['numpy','matplotlib'],
      packages=['biotools', 'biotools.analysis', 'biotools.IO'],
      package_dir={'biotools': 'src'},
      scripts=['prok-geneseek'],
      keywords='gene prediction, prokaryotes, effectors',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
      ])
