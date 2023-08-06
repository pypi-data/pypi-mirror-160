import setuptools

with open("README.md", "r") as fh:
    description = fh.read()
    setuptools.setup(
        name="resilipy",
        version="0.1.0",
        author="Vincent Dietrich",
        author_email="vdietric@students.uni-mainz.de",
        packages=setuptools.find_packages(),
        description="ResiliPy - A machine-learning based Mouse labelling GUI.",
        long_description=description,
        long_description_content_type="text/markdown",
        url="https://github.com/dietvin/resilipy",
        license='MIT',
        python_requires='>=3.8',
        install_requires=[
            "PyQt6>=6.3.1",
            "xgboost>=1.6.1",
            "scikit-learn>=1.1.1",
            "numpy>=1.23.1",
            "pandas>=1.4.3",
            "openpyxl>=3.0.10",
            "Levenshtein>=0.20.1",
            "pyqtgraph>=0.12.4"
        ],
        package_data={
            "resilipy": ["models/XGBoost C57 mice.model", "ui/builder.ui", "ui/labeler.ui", "ui/preprocessor.ui", "ui/resilipy.ui", "ui/stylesheet.txt"]
        },
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering :: Bio-Informatics"
        ]
    )

