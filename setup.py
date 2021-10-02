import setuptools

setuptools.setup(
    name="wykop",
    version="0.0.1",
    description="Wykop Tags",
    packages=setuptools.find_packages(include=['wykop']),
    python_requires='>=3.8',
    install_requires=[
        'requests==2.26.0'
    ]
)

