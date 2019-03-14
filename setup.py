from setuptools import setup

setup(name = 'argoncube2x2ggd',
      version = '2.1.0',
      description = 'ArgonCube2x2 based on General Geometry Description',
      author = 'Hunter Sullivan',
      author_email = 'hunter.sullivan@mavs.uta.edu',
      license = 'GPLv2',
      url = 'https://github.com/hsullivan12/argoncube2x2ggd',
      package_dir = {},
      packages = ['argoncube2x2ggd', 'argoncube2x2ggd.Detector', 'argoncube2x2ggd.DetectorHall', 'argoncube2x2ggd.Config', 'argoncube2x2ggd.Tools', 'argoncube2x2ggd.World'],
      install_requires = [
        "gegede >= 0.4",
        "pint >= 0.5.1",      # for units
        "lxml >= 3.3.5",      # for GDML export],
      ],
  )

