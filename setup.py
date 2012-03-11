from distutils.core import setup
setup(name='pm2534',
      version='0.1',
      author='Tymm Twillman',
      author_email='tymmothy@gmail.com',
      description='Philips PM2534 bench meter control module',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
      ],
      license='BSD-new',
      requires=[
          'gpib_devices',
      ],
      provides=[
          'pm2534',
      ],
      py_modules=[
          'pm2534',
      ],
      )

