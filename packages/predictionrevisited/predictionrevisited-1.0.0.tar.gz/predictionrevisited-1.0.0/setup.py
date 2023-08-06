from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
      name = "predictionrevisited",
      version = "1.0.0",
      author = "Megan Czasonis and David Turkington",
      description = "Prediction Revisited module for observation-based prediction",
      long_description = long_description,
      long_description_content_type = "text/markdown",
      packages = find_packages(),
      license = "MIT",
      url = "https://www.predictionrevisited.com",
      py_modules = ["predictionrevisited"],
      install_requires = ["numpy", "pandas"]
)

