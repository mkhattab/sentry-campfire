from setuptools import setup, find_packages

setup(
    name='sentry_campfire',
    version='0.1.2',
    author='Mustafa Khattab',
    author_email='mustafa.khattab@gmail.com',
    url='https://github.com/mkhattab/sentry-campfire',
    description='A Sentry Campfire notification plugin',
    keywords='sentry-campfire sentry campfire',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'sentry>=4.6.0',
        'requests>=0.12.1',
    ],
    dependency_links=[
        'https://github.com/mlafeldt/camplight/tarball/master#egg=camplight',
    ],
    license = 'BSD',
    include_package_data=True,
    entry_points={
        'sentry.plugins': [
            'campfire = sentry_campfire.plugin:CampfireNotification',
         ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
