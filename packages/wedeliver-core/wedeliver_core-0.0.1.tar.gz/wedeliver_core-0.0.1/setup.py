from setuptools import setup

# reading long description from file
# with open('DESCRIPTION.txt') as file:
#     long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = []

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]

setup(
    name='wedeliver_core',
    version='0.0.1',
    description='weDeliverCore package',
    long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
    long_description_content_type='text/markdown',
    url='https://www.wedeliverapp.com/',
    author='Eyad Farra',
    author_email='info@wedeliverapp.com',
    license='MIT',
    packages=['wedeliver_core'],
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS
)
