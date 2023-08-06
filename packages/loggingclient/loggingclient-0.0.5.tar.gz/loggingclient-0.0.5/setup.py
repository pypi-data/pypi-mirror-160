import setuptools

LONG_DESCRIPTION = "This package will be used primarily in logging data processing pipelines and other such applications."

setuptools.setup(
    name="loggingclient",
    version="0.0.5",
    description="A library to log to the console and other platforms.",
    packages=setuptools.find_packages(),
    py_modules=["loggingclient"],
    long_description=LONG_DESCRIPTION,
    python_requires=">=3.9",
    install_requires=[
        "pylogctx==1.12",
    ],
)
