import setuptools

setuptools.setup(
    name="loggingclient",
    version="0.0.1",
    description="A library to log to console and other platforms.",
    packages=list(set(setuptools.find_packages()) - {"tests"}),
    python_requires=">=3.9",
    install_requires=[
        "pylogctx==1.12",
    ],
)
