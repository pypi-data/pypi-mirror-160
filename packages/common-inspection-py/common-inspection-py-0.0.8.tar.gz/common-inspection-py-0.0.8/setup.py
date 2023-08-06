from distutils.core import setup

setup(
    name='common-inspection-py',
    version='0.0.8',
    author='X.X',
    author_email='xx@example.com',
    url='http://www.example.com/',
    license='LICENSE',
    packages=['common_inspection_py', 'common_inspection_py.config', 'common_inspection_py.interfaces', 'common_inspection_py.types', 'common_inspection_py.utils'],
    description="The description of the package",
    long_description_content_type="text/markdown",
    long_description="test",
    install_requires=['boto3~=1.24.22',
                      'PyYAML',
                      'pandas~=1.4.3',
                      'numpy',
                      'pydantic~=1.9.1'
                      ]
)
