import setuptools

setuptools.setup(
    name="easy-stat",
    version="1.0.0",
    author="s0urce",
    author_email="boyarkin.gleb@gmail.com",
    description="It's easy statistics",
    long_description='https://github.com/s0urcedev/easystatistics - GitHub',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['statistics'],
    install_requires=['matplotlib']
)