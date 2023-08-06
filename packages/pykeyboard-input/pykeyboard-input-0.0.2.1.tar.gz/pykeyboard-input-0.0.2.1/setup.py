from setuptools import setup, find_packages
VERSION = '0.0.2.1'
DESCRIPTION = 'Just a package i used in many projects to get which key pressed from keyboard'
LONG_DESCRIPTION = 'Just a package i used in many projects to get which key pressed from keyboard'

# Setting up
setup(
    name="pykeyboard-input",
    version=VERSION,
    author="Emam_ahsour",
    author_email="emam54637@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pywin32'],
    keywords=['python', 'keyboard', 'tools', 'pycv2', 'inputs'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
