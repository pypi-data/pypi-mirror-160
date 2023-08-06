import setuptools
setuptools.setup(
    name='pypcdp',
    version='0.23',
    author='xgzh',
    author_email="",
    description="PCDP api",
    long_description="PCDP Api",
    #platforms='win32',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    classifiers=[
        'Topic :: Software Development',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers'
    ]

)
