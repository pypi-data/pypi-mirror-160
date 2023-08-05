from setuptools import setup, find_packages
'''
setup(
   name="CDynamics",
   version="1.0.2",
   packages=find_packages(),
   install_requires=['numpy','matplotlib'],
)
'''

VERSION = '1.0.2'
DESCRIPTION = 'Plot Julia sets of rational functions'
LONG_DESCRIPTION = 'A package that allows users to visualize julia sets of rational holormorhphic self-maps defined on the Riemann sphere'

setup(
    name="CDynamics",
    version=VERSION,
    author="Kanak Dhotre",
    author_email="dhotrekanak@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy','matplotlib'],
    keywords=['python', 'complex dynamics', 'julia set', 'filled julia sets'],
)
