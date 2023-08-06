from setuptools import setup

setup(
    name='ReachSample',
    version='0.1.0',
    description='A python library for sampling commands within a robotic workspace, '
                'compatible with the ReachMaster experimental paradigm.',
    url='https://github.com/throneofshadow/ReachSample',
    author='Brett Nelson',
    author_email='bnelson@lbl.gov',
    license='BSD-3-Clause-LBNL',
    packages=['ReachSample'],
    install_requires=['pandas', 'matplotlib.pyplot', 'unittest',
                      'numpy', 'os', 'pdb', 'ffmpeg'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)