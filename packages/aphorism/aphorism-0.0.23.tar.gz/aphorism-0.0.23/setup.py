


# Resources
# ----------------------------------------------------------------------------
# see https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools
# https://www.freecodecamp.org/news/build-your-first-python-package/



# Folder Structure Before Following Directions Below
# ----------------------------------------------------------------------------
# aphorism
# ----aphorism
# --------basic_functions
# ------------__init__.py
# ------------add.py
# ------------divide.py
# ------------multiply.py
# ------------subtract.py
# --------covid_functions
# ------------__init__.py
# ------------add.py
# ------------divide.py
# ------------multiply.py
# ------------subtract.py
# --------dashboard_functions
# ------------__init__.py
# ------------add.py
# ------------divide.py
# ------------multiply.py
# ------------subtract.py
# --------data_collection_functions
# ------------__init__.py
# ------------add.py
# ------------divide.py
# ------------multiply.py
# ------------subtract.py
# --------graphing_functions
# ------------__init__.py
# ------------add.py
# ------------divide.py
# ------------multiply.py
# ------------subtract.py
# --------image_processing_functions
# ------------__init__.py
# ------------add.py
# ------------divide.py
# ------------multiply.py
# ------------subtract.py
# --------__init__.py
# ----latex
# ----sql
# ----setup.cfg
# ----README.md
# ----LICENSE.txt
# ----setup.py



# Directions for uploading
# ----------------------------------------------------------------------------
# make sure twine is installed
#     pip install twine
# change your directory into the main aphorism folder
# run the line below when ready to rebuild the package
#     python setup.py sdist
# make sure things are okay with upload using testpypi; run
#     twine upload --repository testpypi dist/*
# if things check out, run 
#     twine upload dist/*
# when prompted for the user name, use
#     __token__
# when prompted for the password, use the token generated upon registering with PyPi



# Issues with PyPi Uploading
# ----------------------------------------------------------------------------
# The first major issue I had when doing the the update to PyPi was making 
# sure the files haven't existed previously. This was a problem because it was 
# registering versions in dist folder. Removing the build and dist folders 
# fixed the problems after updating the version number.



# The __init__.py files
# ----------------------------------------------------------------------------
# Understanding the __init__.py files has taken a considerable amount of work.
# I am writing this down as a reference for any future person reading this. 

# The __init__.py file only contains import statements for python files in the 
# immediate, same directory. It should not contain import statements for the 
# sub-folders containing __init__.py files. The sub-folders containing 
# __init__.py files should be handled through the 

#     from foo import bar (as alias)

# structure when needed because they are stand alone packages/modules. 

# This is much clearer through an example. Consider the example project below.

# aphorism >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> this is the project level folder
# ----aphorism >>>>>>>>>>>>>>>>>>>>>>>>>> this is the main-package level folder
# --------basic_functions >>>>>>>>>>>>>>> this is a sub-package folder
# ------------__init__.py >>>>>>>>>>>>>>> the __init__.py for sub-package
# ------------inside_module_1.py >>>>>>>> a module inside sub-package
# ------------inside_module_2.py >>>>>>>> a module inside sub-package
# --------outside_module.py >>>>>>>>>>>>> the module inside main-package
# --------__init__.py >>>>>>>>>>>>>>>>>>> the __inti__.py for the main-package
# ----setup.cfg >>>>>>>>>>>>>>>>>>>>>>>>> the main-package configuration file
# ----README.md >>>>>>>>>>>>>>>>>>>>>>>>> the markdown README file
# ----LICENSE.txt >>>>>>>>>>>>>>>>>>>>>>> the licensing file
# ----setup.py >>>>>>>>>>>>>>>>>>>>>>>>>> the specs for PyPi integration
# ----bad_example.py >>>>>>>>>>>>>>>>>>>> we want this to be a module but isn't

# To make this example really concrete, let's give each of these files some 
# contents.

# aphorism/aphorism/outside_module.py contains the function
#     def add_numbers(x,y):
#         return x+y
    
# aphorism/aphorism/basic_functions/inside_module_1.py contains the function
#     def multiply_numbers(x,y):
#         return x*y
    
# aphorism/aphorism/basic_functions/inside_module_2.py contains the function
#     def average_numbers(x,y):
#         return (x+y)/2
    
# aphorism/aphorism/basic_functions/__init__.py contains 
#     from .inside_module_1 import *
    
# aphorism/aphorism/__init__.py contains 
#     from .outside_module import *

# Assuming all of the files and directories shown above exist, perform as 
# expected, passed the setup build, passed the upload to PyPi, and were
# subsequently installed/upgraded via pip, here is how the various import 
# statements will work:
    
#     import aphorism
#         This will make add_numbers() available directly by calling
#         aphorism.add_numbers().
        
#     from aphorism.basic_functions import *
#         This will make multiply_numbers() available directly. Notice that this
#         DOES NOT make average_numbers() available because inside_module_2 was
#         not specified in the aphorism/aphorism/basic_functions/__init__.py 
#         list of imports.
        
#     from aphorism.basic_functions import inside_module_2 as im2
#         This make average_numbers available by calling 
#         im2.average_numbers().



# Upgrading aphorism after PyPi update
# ----------------------------------------------------------------------------
# pip install aphorism --upgrade



from setuptools import setup, find_packages

VERSION='0.0.23' # MAJOR.MINOR.MAINTENANCE 
DESCRIPTION='My first Python package'

with open("README.md", "r", encoding="utf-8") as fh: # just added
    LONG_DESCRIPTION = fh.read() # just added

setup(
    name="aphorism", # name of the package
    version=VERSION, 
    author="Joshua Fetbrandt", # first last
    author_email="abc@gmail.com", # email
    description=DESCRIPTION, # see very top of file
    long_description=LONG_DESCRIPTION, # see very top of file
    long_description_content_type = 'text/markdown', # if we use a markdown version of the description
    license="MIT", # license choice; MIT is least restrictive
    keywords="altair visuals oppe metrics hospital credentialing image text processing python healthcare", # search keywords on PyPi
    url='https://pypi.org/project/aphorism', # direct link to project
    packages=find_packages(),
    classifiers=[ # tags for the project
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Documentation',
        "Intended Audience :: Education",
        # "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[ # add any additional packages that are required
        'numpy',
        'pandas',
        'altair',
        'altair_saver',
        'selenium',
        'html2pdf', # just added
        'opencv-python', # just added
        # 'tkinter', # just added
        # 'pathlib', # just added
        # 'pyarrow', # just added
        # 'fastparquet', # just added
        # 'imutils', # just added
        # 'PIL', # just added
        # 'import-ipynb', # just added
        # 'pyproj', # just added
        # 'fiona', # just added
        # 'shapely', # just added
        # 'geopandas', # just added
        # 'pkg-resources', # just added
    ], 
    python_requires='>=3',
    include_package_data=True, # just added
    package_data={'': ['examples/*.csv','examples/*.txt','examples/*.sql',
                       'examples/*.tex','examples/*.ipynb','examples/*.parq',
                       'examples/*.parquet','examples/*.xlsx',
                       'examples/*.xls',]}, # just added
    
    # project_urls={
    #     'Developer GitHub': 'https://github.com/joshuafetbrandt/joshuafetbrandt'
    #     # 'Documentation': '', # 'https://packaging.python.org/tutorials/distributing-packages/'
    #     # 'Funding': '', # 'https://donate.pypi.org'
    #     # 'Say Thanks!': '', # 'http://saythanks.io/to/example'
    #     # 'Source': '', # 'https://github.com/pypa/sampleproject/'
    #     # 'Tracker': '', # 'https://github.com/pypa/sampleproject/issues'
    # }
    # data_files=[('my_data', ['data/data_file'])],
    # package_data={
    #     'sample': ['package_data.dat'],
    # },
    
)