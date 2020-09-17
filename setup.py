from setuptools import setup, find_packages

setup (
    name = 'ocp-api-consumer',
    version='0.8.0',
    description='OpenShift python client',
    url='https://github.bancogalicia.com.ar/devo-devops/',
    author='ivan Molinari',
    author_email='Ivan.Molinari@bancogalicia.com.ar',
    keywords='openshift api client',
    include_package_data=True,
    packages=find_packages()
)
