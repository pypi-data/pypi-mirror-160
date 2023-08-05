from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='fedexrates',
    packages=['fedexrates'],  # this must be the same as the name above
    version='0.1',
    description='Libreria para conseguir cotizaciones sobre envio de paquetes con la API de shipengine (FedEx)',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Luis Contreras',
    author_email='desarrollo02@cebsa.mx',
    # use the URL to the github repo
    url='https://github.com/luisandresgc/fedexrates',
    download_url='https://github.com/luisandresgc/fedexrates/tarball/0.1',
    keywords=['testing', 'logging', 'example'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)