from setuptools import setup, find_packages

setup(
    name='cyla_mixture',
    include_package_data=True,
    # package_data={
    #     'src': ['design.ui'],
    # },
    version='1.0',
    # package_dir={'': 'src'},
    packages=find_packages(),
    # packages=[
    #     '__init__',
    #     '__main__',
    #     'cyla_mixture'
    # ],
    install_requires=[
        'PyQt5'
    ],
    # py_modules=['main'],
    url='https://github.com/Hattiffnat/cyla_mixture.git',
    license='LICENSE',
    author='hattiffnat',
    author_email='sereyfeam@gmail.com',
    description='Replaces some Cyrillic letters with similar Latin ones.',
    long_description='file: README.md',
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'gui_scripts': [
            'cyla = cyla_mixture.application:main'
        ]
    },
)
