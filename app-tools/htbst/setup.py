from setuptools import setup, find_packages

setup(
    name='htbst',
    author='replican',
    description="unoficcial htb library",
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'asyncio'
    ],
    entry_points={
        'console_scripts': [
            'htbst-cli = htbst.main:main',  
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
