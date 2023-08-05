from setuptools import setup
import os

readme = open("./README.md", "r")

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

def load_requirements(fname):
    reqs = parse_requirements(fname, session=False)
    return [str(ir.requirement) for ir in reqs]

setup(
    name='fedexrates',
    install_requires=load_requirements("requirements.txt"),
    packages=['fedexrates', ],  # this must be the same as the name above
    version='0.5',
    description='Libreria para conseguir cotizaciones sobre envio de paquetes con la API de shipengine (FedEx)',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Luis Contreras',
    author_email='desarrollo02@cebsa.mx',
    # use the URL to the github repo
    url='https://github.com/luisandresgc/fedexrates',
    download_url='https://github.com/luisandresgc/fedexrates/tarball/0.5',
    keywords=['testing', 'logging', 'example'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)