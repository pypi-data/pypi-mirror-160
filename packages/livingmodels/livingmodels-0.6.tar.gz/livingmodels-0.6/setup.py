from setuptools import setup, find_packages

setup(name='livingmodels',
      version='0.6',
      description='Models for global admin',
      packages=find_packages('app/models'),
      package_dir={'': 'app/models'},
      author_email='777koba@mail.ru',
      install_requires=[
            'requests', 'SQLAlchemy == 1.4.39',
            'importlib-metadata; python_version == "3.10"',
      ],
      zip_safe=False)
