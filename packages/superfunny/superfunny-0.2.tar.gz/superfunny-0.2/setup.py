#!/usr/bin/env python3.6.3a
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
       long_description = fh.read()

setup(name='superfunny',
      version='0.2',
      description='The funniest joke in the world',
      long_description=long_description,
      long_description_content_type="text/markdown",
#      classifiers=[
#        'Development Status :: 3 - Alpha',
#        'License :: OSI Approved :: MIT License',
#        'Programming Language :: Python :: 2.7',
#        'Topic :: Text Processing :: Linguistic',
#      ],
#      keywords='funniest joke comedy flying circus',
      url='http://github.com/melaniecheah/test_repo',
      author='Melanie Cheah',
      author_email='melaniecheah@example.com',
      license='MIT',
      packages=['superfunny'],
      install_requires=[
          'markdown',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['funniest-joke=superfunny.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
