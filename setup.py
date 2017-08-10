from setuptools import setup

setup(
    name='af-words-clustering',
    version='0.1.0',
    description='Affinity propagation for words',
    license="MIT",
    author='Jakub Kawa',
    author_email='kuba.kawa@hotmail.com',
    url="https://github.com/Superzer0/TDA.Python",
    keywords='clustering words affinity propagation',
    packages=['console', 'objects', 'services', 'console.example_dataset'],
    install_requires=['distance', 'numpy', 'scikit-learn', 'stemming'],

    package_data={
        'console.example_dataset': ['example.txt'],
    },
    entry_points={
        'console_scripts': [
            'console=af_cluster:run',
        ]
    }
)
