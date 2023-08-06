from setuptools import setup, find_packages

classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
    
                ]


setup(
    name='zola_ugrid_control',
    version='0.0.2',
    description='Basic control library',
    url='',
    author_email='Francisco.ulloa@zolaelectric.com',
    license='MIT',
    classifiers=classifiers,
    keywords='ugrid control library',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pymodbus'
    ]
)