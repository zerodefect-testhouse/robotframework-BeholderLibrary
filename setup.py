from pathlib import Path
from setuptools import find_packages, setup

CUR_DIR = Path(__file__).parent

with open(Path.joinpath(CUR_DIR, "README.md"), "r") as fh:
    long_description = fh.read()


setup(
    name                 = 'robotframework-dejavu',  
    version              = '0.1.0',
    keywords             = 'robotframework testing testautomation visualregression selenium webdriver web',
    package_dir          = {'': 'src'},
    packages             = find_packages('src'),
    package_data         = {"DejavuLibrary": 
                                ['*.py']
                            },
    install_requires     = [
                            'requests>=2.27.1',
                            'robotframework>=5.0.1',
                            'robotframework-seleniumlibrary>=6.0.0'
                           ],
    include_package_data = True,
    author               = "Zero-Defect Test House",
    author_email         = "centro.tecnologia@zero-defect.com.br",
    description          = "A Robot Framework package to integrate with Dejavu, the Zero-Defect's Visual Regression Testing platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zerodefect-testhouse/robotframework-DejavuLibrary",
    classifiers          = [
                            "Programming Language :: Python :: 3",
                            "License :: OSI Approved :: MIT License",
                            "Operating System :: OS Independent",
                            "Topic :: Software Development :: Testing",
                            "Framework :: Robot Framework",
                            "Framework :: Robot Framework :: Library"
                           ],
    )