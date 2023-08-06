import setuptools

setuptools.setup(
    name="artemis_labs",
    version="0.0.9",
    author="Artemis Labs",
    author_email="austinmccoy@artemisar.com",
    description="Artemis Labs",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    install_requires=[
        'imageio',
        'websockets'
    ]
)