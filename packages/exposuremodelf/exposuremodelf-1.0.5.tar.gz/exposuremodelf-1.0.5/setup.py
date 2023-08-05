
import setuptools
setuptools.setup(
    name="exposuremodelf",
    version="1.0.5",

    author="Sha",
    author_email="sliu23009@gmail.com",
    packages=setuptools.find_packages(),
    install_requires=["torch", "Pillow", "torchvision"],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    package_data={'': ['src/exposuremodelf/model.pth']},
)