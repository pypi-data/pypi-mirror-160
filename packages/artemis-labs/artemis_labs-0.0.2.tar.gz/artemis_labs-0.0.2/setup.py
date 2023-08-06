import setuptools

setuptools.setup(
    name="artemis_labs",
    version="0.0.2",
    author="Artemis Labs",
    author_email="austinmccoy@artemisar.com",
    description="Artemis Labs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    install_requires=[
        'imageio',
        'websockets'
    ]
)