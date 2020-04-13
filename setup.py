import setuptools


long_description = ("This SDK simplifies programmatic usage of DataSource in Python applications.")

setuptools.setup(
    name="datasource_python",
    version="0.0.1",
    author="Bocks",
    description="DataSource Python SDK",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/bocks-ds/datasource-python",
    packages=setuptools.find_packages(),
    install_requires=[
            'pycurl'
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
