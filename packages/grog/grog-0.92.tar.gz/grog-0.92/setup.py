import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grog",
    version="0.92",
    author="Georges Da Costa",
    author_email="georges.da-costa@irit.fr",
    description="GeneRic wOrkload Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.irit.fr/sepia-pub/grog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['matplotlib', 'pytz', 'numpy'],
    entry_points={
        'console_scripts': [
            'grog-tool = grog.grog:main',
        ]
    }
)
