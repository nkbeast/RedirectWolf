from setuptools import setup, find_packages

setup(
    name='redirectwolf',
    version='1.0.0',
    description='Asynchronous Open Redirect Vulnerability Scanner',
    author='NK',
    author_email='naveenbeastyt@gmail.com',
    url='https://github.com/nkbeast/RedirectWolf',
    packages=find_packages(),
    py_modules=['redirectwolf'],
    entry_points={
        'console_scripts': [
            'redirectwolf = redirectwolf:main',
        ],
    },
    install_requires=[
        'httpx>=0.24.0',
        'click>=8.1',
        'PyYAML>=6.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
