import setuptools

LONG_DESCRIPTION = 'This package will be used primarily in logging data processing pipelines and other such applications.'

setuptools.setup(
    name="loggingclient",
    version="0.0.2",
    description="A library to log to console and other platforms.",
    packages=["loggingclient.logs"],
    long_description=LONG_DESCRIPTION,
    python_requires=">=3.9",
    install_requires=[
        "pylogctx==1.12",
    ],
)
