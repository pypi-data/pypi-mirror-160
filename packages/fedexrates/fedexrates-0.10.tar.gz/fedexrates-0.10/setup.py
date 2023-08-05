from setuptools import setup
import os

def check_dependencies():
    install_requires = []

    # Assuming the python standard library is installed...
    try:
        import certifi
    except ImportError:
        install_requires.append('certifi')

    try:
        import idna
    except ImportError:
        install_requires.append('idna')

    try:
        import requests
    except ImportError:
        install_requires.append('requests')

    try:
        import urllib3
    except ImportError:
        install_requires.append('urllib3')

    return install_requires


readme = open("./README.md", "r")

# lib_folder = os.path.dirname(os.path.realpath(__file__))
# requirement_path = lib_folder + '/requirements.txt'
# install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
# if os.path.isfile(requirement_path):
#     with open(requirement_path) as f:
#         install_requires = f.read().splitlines()

install_requires = check_dependencies()


setup(
    name='fedexrates',
    packages=['fedexrates'],  # this must be the same as the name above
    install_requires=install_requires,
    version='0.10',
    description='Libreria para conseguir cotizaciones sobre envio de paquetes con la API de shipengine (FedEx)',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Luis Contreras',
    author_email='desarrollo02@cebsa.mx',
    # use the URL to the github repo
    url='https://github.com/luisandresgc/fedexrates',
    download_url='https://github.com/luisandresgc/fedexrates/tarball/0.10',
    keywords=['testing', 'logging', 'example'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)