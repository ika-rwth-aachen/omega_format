import setuptools
import sys
import versioneer

install_requires = [
    'numpy',
    'h5py',
    'tqdm',
    'typer',
    'xarray',
    'pydantic<=2.0.0',
    'parse',
    'shapely'
]
extras_require = {
    'visualization': ['pyqtgraph', 'pyqt5'],
    'doc': ['pdoc3'],
    'test': ['pytest']
}
extras_require["complete"] = sorted({v for req in extras_require.values() for v in req})

with open("README.md", "r", encoding="utf8", errors='ignore') as f:
    long_description = f.read()

setuptools.setup(
    name='omega_format',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="ika - RWTH Aachen",
    author_email="michael.schuldes@ika.rwth-aachen.de",
    description="OMEGA Format Library (read/write/visualize)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ika-rwth-aachen/omega_format",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: None",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'omega_format = omega_format.cli:app',
        ],
    },
    install_requires=install_requires,
    extras_require=extras_require,
    include_package_data=True,
    zip_safe=False
)
