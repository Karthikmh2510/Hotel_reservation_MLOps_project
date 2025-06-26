from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS_hotel_reservation",
    version="0.1.0",
    author="Karthik Manjunath Hadagali",
    packages=find_packages(),
    install_requires=requirements,
    description="A project to predict hotel reservation cancellations using machine learning.",
)