from setuptools import setup

setup(name='livingmodels',
      version='0.4',
      description='Models for global admin',
      packages=['livingmodels/models'],
      author_email='777koba@mail.ru',
      install_requires=[
            'requests', 'SQLAlchemy == 1.4.39',
            'importlib-metadata; python_version == "3.10"',
      ],
      zip_safe=False)
