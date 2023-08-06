import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Spoonful',                        # should match the package folder
    packages=setuptools.find_packages(),                          # should match the package folder
    version='0.0.1',                                # important for updates
    license='MIT',                                  # should match your chosen license
    description='Basic Tools in Numerical Methods',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Nikhil Murali',
    author_email='nikhilmurali1301@gmail.com',
    url='https://github.com/m3mc3/Spoonful.git', 
# =============================================================================
#     project_urls = {                                # Optional
#         "Bug Tracker": "https://github.com/mike-huls/toolbox_public/issues"
#     },
# =============================================================================
    install_requires=['matplotlib','numpy'],                  # list all packages that your package uses
    keywords=["pypi", "spoonful", "scientific"],    #descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)