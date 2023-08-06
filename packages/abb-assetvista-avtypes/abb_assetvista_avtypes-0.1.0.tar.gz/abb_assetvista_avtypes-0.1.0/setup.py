import setuptools

install_requires=[]
install_requires.append('pint')

setuptools.setup(
    name="abb_assetvista_avtypes",
    version="0.1.0",
    author="Tiago Prata",
    author_email="tiago.prata@br.abb.com",
    description="Package defining the classes and methods required for using the ABB AssetVista library on the Genix Streaming Calculation Engine.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.6',
    install_requires=install_requires
)