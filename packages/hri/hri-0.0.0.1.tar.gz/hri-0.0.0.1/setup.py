from setuptools import setup
#from distutils.core import setup

setup(
    name='hri',
    version='0.0.0.1',
    author='Enrique Coronado',
    author_email='enriquecoronadozu@gmail.mx',
    url='http://enriquecoronadozu.github.io',
    description='NEP additional packages',
    packages=["hri"],
    install_requires=[
          'nep', 'mediapipe'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development"
    ]
)

