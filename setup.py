import io

from setuptools import find_packages, setup

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="tunnel_rpc",
    version="0.0.1",
    license="MIT",
    maintainer="Lauren Vagts, Luke Smith, Wyatt Huskey",
    maintainer_email="lsmith@zenoscave.com",
    description="Tunnel RPC",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["docker==3.7.0", "Flask==1.0.2", "jsonrpcserver==4.0.1"],
    console_scripts=[],
    extras_require={
        "test": [
            "coverage",
            "flake8",
            "pylint",
            "pytest",
            "sphinx",
            "sphinxcontrib.napoleon",
        ]
    },
)
