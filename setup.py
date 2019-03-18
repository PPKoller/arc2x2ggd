from setuptools import setup

setup(name = 'arc2x2ggd',
      version = '1.0.0',
      description = 'ArgonCube2x2 based on General Geometry Description',
      author = 'Patrick Koller and Hunter Sullivan',
      author_email = 'patrick.koller@lhep.unibe.ch, hunter.sullivan@mavs.uta.edu',
      license = 'GPLv2',
      url = 'https://github.com/hsullivan12/arc2x2ggd',
      package_dir = {},
      packages = ['arc2x2ggd', 'arc2x2ggd.Detector', 'arc2x2ggd.DetectorHall', 'arc2x2ggd.Config', 'arc2x2ggd.Tools', 'arc2x2ggd.World'],
      install_requires = [
        "gegede >= 0.4",
        "pint >= 0.5.1",      # for units
        "lxml >= 3.3.5",      # for GDML export],
      ],
  )

