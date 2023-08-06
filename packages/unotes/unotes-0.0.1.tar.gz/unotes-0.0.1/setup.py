from distutils.core import setup
setup(
  name = 'unotes',        
  packages = ['src'], 
  version = '0.0.1',      
  license='MIT',        #- Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Grab notes from internet.',   #- - Give a short description about your library
  author = 'Utsab kafle',                   #- Type in your name
  author_email = 'utshubkaphle@gmail.com',      #- Type in your E-Mail
  url = 'https://github.com/UtsabKafle/unotes',   #- Provide either the link to your github or to your website
  download_url = 'https://github.com/UtsabKafle/unotes/archive/refs/tags/v_0.0.1.tar.gz',    #- I explain this later on
  keywords = ['unotes', 'scrapping', 'notes','assignment'],   #- Keywords that define your package best
  install_requires=[            #- I get to this in a second
          'wikipedia',
          'beautifulsoup4',
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      #- Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      #- Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   #- Again, pick a license
    'Programming Language :: Python :: 3',      #-Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)