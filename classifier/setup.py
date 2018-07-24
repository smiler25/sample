try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='classifier_example',
    version='0.1',
    py_modules=['classifier'],
    url='https://github.com/smiler25/samples/classifier',
    author='Anton Kolosov',
    author_email='kolosmile@yandex.ru',
    description='',
    test_suite='test_classifier',
)
