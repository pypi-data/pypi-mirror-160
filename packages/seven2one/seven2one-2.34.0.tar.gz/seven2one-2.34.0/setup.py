from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(name='seven2one',
      version='2.34.0',
      description='Functions to interact with the Seven2one TechStack',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://www.seven2one.de',
      author='Seven2one Informationssysteme GmbH',
      author_email='info@seven2one.de',
      license='MIT',
      packages=['seven2one', 'seven2one.utils'],
      include_package_data=True,
      install_requires=[
            'pandas', 'gql==3.0.0', 'pytz', 'tzlocal', 'pyperclip', 'loguru', 'requests', 'requests_toolbelt'
            ],
      classifiers =[
            'Development Status :: 3 - Alpha',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            ],
      python_requires='>=3.6',
      zip_safe=False)