"""
py setup.py sdist
twine upload dist/expressmoney-points-1.17.16.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney-points',
    packages=setuptools.find_packages(),
    version='1.17.16',
    description='Service points',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('expressmoney>=11.0.4', 'django-money'),
    python_requires='>=3.7',
)
