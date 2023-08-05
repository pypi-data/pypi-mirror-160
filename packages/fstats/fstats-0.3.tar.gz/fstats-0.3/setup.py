from setuptools import setup, find_packages

setup(
    name='fstats',
    version="0.3",
    author="bbing",
    install_requires=['psutil'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'fstats = fstats.__main__:main'
        ]
    }
)
