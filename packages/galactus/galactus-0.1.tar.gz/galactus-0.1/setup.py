from setuptools import setup, find_packages


setup(
    name='galactus',
    version='0.1',
    license='MIT',
    author="Olwethu Sigwela",
    author_email='olwethus10@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/ratt-ru/mining-boom',
    keywords='anomaly detection', 
    install_requires=[
          'scikit-learn', 
          'matplotlib', 
          'numpy', 
          'pandas', 
          'radiopadre',
          'scipy',
          'seaborn'
      ],

)