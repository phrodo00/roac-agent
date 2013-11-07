from setuptools import setup
import sys

if 'bdist_rpm' in sys.argv:
    data_files = [('/etc/', ['examples/centos/etc/roac.cfg']),
                  ('/etc/sysconfig/', ['examples/centos/etc/sysconfig/roacd']),
                  ('/etc/init/', ['examples/centos/etc/init/roacd.conf',
                                  'examples/centos/etc/init/roacd_root.conf']),
                  ('/var/lib/roac/scripts', ['examples/scripts/*'])
                  ]
else:
    data_files = [('examples', ['examples/centos']),
                  ('scripts', ['examples/scripts'])]

setup(name='roac',
      packages=['roac', 'roac.extra'],
      scripts=['bin/roacd'],
      data_files=data_files,
      version='0.0.1',
      description='System monitoring agent framework',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX',
          'Topic :: Software Development :: Libraries :: Application Frameworks',
          'Topic :: System :: Monitoring'],
      url='https://github.com/roac-monitoring/roac-agent',
      author='Javier Aravena Claramunt',
      author_email='javier@aravenas.com',
      license='BSD',
      zip_safe=False
      )
