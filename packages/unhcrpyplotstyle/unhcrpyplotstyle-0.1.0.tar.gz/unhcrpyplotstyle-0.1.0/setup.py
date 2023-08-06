import os
from setuptools import setup

# Get description from README
root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup( name='unhcrpyplotstyle',
       version='0.1.0',
       author='Lei Chen',
       author_email="chen@unhcr.org",
       description="Set matplotlib style following UNHCR's Data Visualization Guidelines",
       packages=['unhcrpyplotstyle'],
       long_description = long_description,
       long_description_content_type='text/markdown',
       license="MIT",
       keywords=[
        "matplotlib-style-sheets",
        "unhcr-plot-style",
        "matplotlib-styles",
        "python"
       ],
       url="https://github.com/leichen88/unhcrpyplotstyle",
       install_requires=['matplotlib>=3.1.0'],
       include_package_data=True
    )