from setuptools import setup, find_packages
import pathlib

# here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
# long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='matialvarezs_handlers_easy',
    version='0.1.67',
    description='Easy handler functions',
    # include_package_data=True,
    author='Matias Alvarez Sabate',
    author_email='matialvarezs@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(where="src"),
    # packages=['matialvarezs_handlers_easy'],  # this must be the same as the name above
    python_requires=">=3.7, <4",
    install_requires=[
        'django-json-response',
        'celery',
        'django-celery-results',
        'arrow',
        'python-dateutil',
        'pytz',
        'python-crontab',
        'paho-mqtt'
    ],
)


# from distutils.core import setup
# import setuptools
#
# setuptools.setup(
#     name='matialvarezs_handlers_easy',
#     packages=setuptools.find_packages(),  # this must be the same as the name above
#     version='0.1.40',
#     install_requires=[
#         'django-json-response==1.1.3',
#         'celery==4.1.0',
#         'django-celery-results==1.0.1',
#         'arrow==0.13.1',
#         'python-dateutil==2.8.0',
#         'pytz',
#         'python-crontab'
#     ],
#     include_package_data=True,
#     description='Easy handler',
#     author='Matias Alvarez Sabate',
#     author_email='matialvarezs@gmail.com',
#     classifiers=[
#         'Programming Language :: Python :: 3.5',
#     ],
# )
