from distutils.core import setup

setup(
    name='curriedef',
    packages = ['curriedef'],
    version='0.1.0',
    description='Currying facade for Python',
    url='https://github.com/kaiserthe13th/curriedef',
    download_url = 'https://github.com/kaiserthe13th/curriedef/archive/refs/tags/0.1.0.tar.gz',
    author='kaiserthe13th',
    author_email='superkerem13@gmail.com',
    keywords = [],
    license='MIT',

    # Dependencies
    install_requires=[],

    classifiers=[
        'Development Status :: 3 - Alpha', # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # List of supported Python versions
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

