from setuptools import find_packages, setup

setup(
    name="random_utilities",
    version="1.0.4",
    author="Hetchfund.Capital (Libby Lebyane)",
    author_email="<lebyane.lm@gmail.com>",
    description="Helper library for random operations",
    # package_dir={"": "random_utilities"},
    packages=["random_utilities", "random_utilities.models"],
    install_requires=["console", "months", "pymongo", "pymongo[srv]"],
    keywords=["random", "utilities", "tools", "helpers"]
)
