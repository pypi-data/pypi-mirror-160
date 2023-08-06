import setuptools

setuptools.setup(
    name="workforcesim",
    version="0.3.15",
    url="https://github.com/NeuraXenetica/synaptans-workforcesim",
    author="Matthew E. Gladden",
    author_email="matthew.gladden@neuraxenetica.com",
    description="Synaptans WorkforceSim is a free open-source platform for generating synthetic data that simulate the dynamics of a factory workforce; employing diverse forms of machine learning to identify trends and correlations and make predictions regarding workers' behavior; and then assessing the accuracy of such AI-based approaches to predictive workplace analytics.",
    packages=['workforcesim'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
    ],
    include_package_data=True,
    package_data={'': ['input_files/*.*']},
    install_requires=[
        'openpyxl',
    ],
)