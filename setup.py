from setuptools import setup, find_packages

setup(
    name="transcendence",
    version="1.0.0",
    description=(
        "A Python framework modelling recursive epistemic self-improvement "
        "and the progressive stages of transcendent intelligence."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="TIA Project",
    python_requires=">=3.9",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Philosophy",
    ],
    entry_points={
        "console_scripts": [
            "transcendence=main:run",
        ],
    },
)
