from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig
from setuptools import setup, find_packages
import os


class register(register_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')

class upload(upload_orig):

    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


setup(
    name='ganesha_experimental',
    version='5.0.0',
    author='Elazar Chodjayev',
    author_email='zenmyx@gmail.com',
    packages=find_packages(),
    cmdclass={
        'register': register,
        'upload': upload,
    }
)
