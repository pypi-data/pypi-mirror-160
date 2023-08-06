import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

top_dir, _ = os.path.split(os.path.abspath(__file__))

if os.path.isfile(os.path.join(top_dir, 'Version')):
    with open(os.path.join(top_dir, 'Version')) as f:
        version = f.readline().strip()
else:
    import urllib
    Vpath = 'https://raw.githubusercontent.com/Nikeshbajaj/phyaat/master/Version'
    version = urllib.request.urlopen(Vpath).read().strip().decode("utf-8")

setuptools.setup(
    name="phyaat",
    version= version,
    author="Nikesh Bajaj",
    author_email="bajaj.nikkey@gmail.com",
    description="PhyAAt: Physiology of Auditory Attention",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://phyaat.github.io",
    packages=setuptools.find_packages(),
    license = 'MIT',
    keywords = 'phyaat auditory-attention attention eeg physiological-signals physiology predictive-analysis artifact EEG EDA Biomedical-signals Electroencephalogram Galvanic-Skin-Response GSR photoplethysmogram PPG',
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Development Status :: 5 - Production/Stable',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    project_urls={
    'Documentation': 'https://phyaat.readthedocs.io/',
    'Say Thanks!': 'https://github.com/Nikeshbajaj',
    'Source': 'https://phyaat.github.io',
    'Tracker': 'https://github.com/Nikeshbajaj/phyaat/issues',
    },
    include_package_data=True,
    install_requires=['numpy','scipy','matplotlib','spkit']
)
