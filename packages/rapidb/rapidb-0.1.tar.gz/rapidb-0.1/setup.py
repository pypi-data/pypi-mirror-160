import setuptools


setuptools.setup(
    name="rapidb",
    version="0.1",
    author="Francis B. Lavoie",
    author_email="francis.b.lavoie@usherbrooke.ca",
    description="Fast DB handler",
    long_description="Fast DB handler",
    long_description_content_type="text/markdown",
    url="https://catalyseur.ca",
    packages=setuptools.find_packages(),
    dependencies = ["mariadb","pyodbc"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)