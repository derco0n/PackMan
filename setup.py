from setuptools import setup

entry_points = {
    "console_scripts": [
        "packman = PackMan.__init__"
    ]
}

setup(
    name='PackMan',
    version='0.13',
    packages=['PackMan'],
    url='https://github.com/derco0n/PackMan',
    entry_points=entry_points,
    install_requires=[
        "mysqlclient==1.3.7",
        "RPi.GPIO==0.6.3",
    ],
    license='GPL v3',
    author='D. Marx',
    author_email='',
    description=''
)
