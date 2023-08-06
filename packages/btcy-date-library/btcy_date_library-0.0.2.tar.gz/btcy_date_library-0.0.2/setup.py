from distutils.core import setup

setup(
    name='btcy_date_library',
    packages=['btcy_date_library'],
    version='0.0.2',
    license='MIT',
    author='Trong Pham',
    install_requires=[
        'python-dateutil'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
