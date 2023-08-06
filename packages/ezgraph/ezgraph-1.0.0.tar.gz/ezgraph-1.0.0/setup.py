from setuptools import setup, find_packages


setup(
    name='ezgraph',
    version='1.0.0',
    license='MIT',
    author="Tamas Nemes",
    author_email='guidewalk.geraet@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Totemi1324/ezgraph/',
    keywords='graph network visualization',
    install_requires=[
          'bokeh',
      ],
)
