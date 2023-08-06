from distutils.core import setup
#started with http://peterdowns.com/posts/first-time-with-pypi.html and then i switched to twine

import sys
if sys.version_info <= (2,7):
  sys.exit("Sorry, Python <= 2.7 is not supported")
elif sys.version_info != (3,9):
  print('Python versions other than 3.9 are untested')

setup(
  name = 'icon_image',
  packages = ['icon_image'], # this must be the same as the name above
  version = '0.0.2',
  description = 'Generate icons programmatically in Python. Helps nudge AI algorithms',
  author = 'Sports Data Direct',
  author_email = 'matteo@matteohoch.com',
  url = 'https://github.com/rogerfitz/icon-image', # use the URL to the github repo
  download_url = 'https://github.com/rogerfitz/icon-image/releases', # git push --tags origin master
  keywords = ['icon','CLIP','GAN',], # arbitrary keywords
  classifiers = [],
  install_requires=[
          "Pillow==9.2.0",
          "icon-font-to-png==0.4.1",
          "numpy==1.22.3",
      ]
)