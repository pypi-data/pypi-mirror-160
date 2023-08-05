import setuptools

DEPENDENCIES = [
]

setuptools.setup(
    name='TriggerManager',
    version='0.2.0',
    description='',
    license='MIT',
    author='Inspide S.L.',
    url='',
    # scripts=['bin/metatron', 'bin/minion', 'bin/webserver'],
    install_requires=DEPENDENCIES,
    packages=setuptools.find_packages(),
    test_suite="nose.collector",
    python_requires=">=3.10"
)