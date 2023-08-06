from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
        'pip   >= 22.1.2',
        'wheel >= 0.37.1',
        'twine >= 4.0.1',
        'ase   >= 3.22.1',
        ]

setup(
    name='AtomicAI',
    version='0.0.1',
    token='selva',
    author='Selva Chandrasekaran',
    author_email='selvachandrasekar.s@gmail.com',
    description='Processing and visualization of atomic coordinates',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/SelvaGith/AtomicAI',
    project_urls = {
        "Bug Tracker": "https://github.com/SelvaGith/AtomicAI/issues"
    },
    license='MIT',


    #packages=['AtomicAI'], #find_packages(),
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.9',
    install_requires= install_requires, #open('requirements.txt').read(), 
    entry_points={'console_scripts': [
        'cq2vasp=AtomicAI.tools.cq2vasp:cq2vasp',
        'vasp2cif=AtomicAI.tools.vasp2cif:vasp2cif',
        'vasp2cq=AtomicAI.tools.vasp2cq:vasp2cq',
        'plt_md_stats=AtomicAI.tools.plt_md_stats:plt_md_stats',
        'rdf=AtomicAI.tools.rdf:RDF',



                                    ]},
)
