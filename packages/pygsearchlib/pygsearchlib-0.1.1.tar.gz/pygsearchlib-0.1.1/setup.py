from distutils.core import setup
setup(
  name = 'pygsearchlib',         # How you named your package folder (MyLib)
  packages = ['pygsearchlib'],   # Chose the same as "name"
  version = '0.1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Library for getting/scraping news from google news',   # Give a short description about your library
  author = 'Roshaan Mehmood',                   # Type in your name
  author_email = 'roshaan55@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/roshaan55/pyweatherlib',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/roshaan55/pygsearchlib/archive/refs/tags/v0.1.tar.gz',    # I explain this later on
  keywords = ['weather', 'open weather map', 'weather api'],   # Keywords that define your package best
  install_requires=[
         'requests', 'bs4'               # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
