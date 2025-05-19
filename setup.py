from setuptools import setup, find_packages

setup(
    name="klavis",
    version="0.1.0",
    author="Valerio Poggi",
    description="Modular MIDI event server and routing framework",
    packages=find_packages(),  # <-- nessun `where="src"` necessario
    install_requires=[],
    extras_require={
        "realtime": ["python-rtmidi"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "klavis-run = klavis.cli:main"
        ]
    }
)

