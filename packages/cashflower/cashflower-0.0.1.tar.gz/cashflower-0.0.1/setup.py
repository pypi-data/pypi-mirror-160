from setuptools import setup, find_packages

setup(
    author="Zuzanna Chmielewska",
    description="Framework for actuarial cash flow models.",
    name="cashflower",
    version="0.0.1",
    packages=find_packages(include=["cashflower", "cashflower.*"]),
    install_requires=[
        "numpy>=1.23.0",
        "pandas>=1.4.3"
    ],
)
