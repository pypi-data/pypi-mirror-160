from setuptools import setup, find_packages

setup(
    name='workhourcalc',
    version='0.0.1',
    description="Calculate working hours",
    long_description='Gets the input opening and closing time of restaurants in millisecond and writes the working '
                     'hours intervals in human readable format',
    url='https://github.com/rasindulakkitha/calc_work_hours',
    author='Rasindu Wanigasinghe',
    author_email='rasindulakkitha95@gmail.com',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    keywords='work_hour',
    packages=find_packages(exclude=('tests*', 'testing*')),
    install_requires=['arrow','jsonschema']
)
