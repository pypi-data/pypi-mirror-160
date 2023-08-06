# -*- coding: UTF-8 -*-
# Copyright 2013-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# test:  $ python setup.py test -s tests.PackagesTests


SETUP_INFO = dict(
    name='lino-voga',
    version='22.7.0',
    install_requires=[
        'lino_xl'
    ],
    test_suite='tests',
    # tests_require=['pytest'],
    description="A Lino Django application for managing courses, "
                "participants and meeting rooms",

    long_description="""\

Lino Voga is a `Lino <https://www.lino-framework.org>`__ application
for managing courses, participants and meeting rooms.

- The central project homepage is https://voga.lino-framework.org

- Online demo site at https://voga1e.lino-framework.org
  and https://voga1r.lino-framework.org

- Technical specs are at https://www.lino-framework.org/specs/voga

- This is an integral part of the Lino framework, which is documented
  at https://www.lino-framework.org

- The changelog is at https://www.lino-framework.org/changes

- For introductions, commercial information and hosting solutions
  see https://www.saffre-rumma.net

- This is a sustainably free open-source project. Your contributions are
  welcome.  See https://community.lino-framework.org for details.

""",
    author='Rumma & Ko Ltd',
    author_email='info@lino-framework.org',
    url="https://gitlab.com/lino-framework/voga",
    license_files=['COPYING'],
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 4 - Beta
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Education
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
Topic :: Office/Business :: Financial :: Accounting
Topic :: Office/Business :: Scheduling
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_voga',
    'lino_voga.lib',
    'lino_voga.lib.cal',
    'lino_voga.lib.cal.fixtures',
    'lino_voga.lib.contacts',
    'lino_voga.lib.contacts.fixtures',
    'lino_voga.lib.contacts.management',
    'lino_voga.lib.contacts.management.commands',
    'lino_voga.lib.courses',
    'lino_voga.lib.courses.fixtures',
    'lino_voga.lib.products',
    'lino_voga.lib.invoicing',
    'lino_voga.lib.invoicing.fixtures',
    'lino_voga.lib.roger',
    'lino_voga.lib.roger.courses',
    'lino_voga.lib.roger.courses.fixtures',
    'lino_voga.lib.roger.courses.management',
    'lino_voga.lib.roger.courses.management.commands',
    'lino_voga.lib.rooms',
    'lino_voga.lib.sales',
    'lino_voga.lib.sales.fixtures',
    'lino_voga.lib.voga',
    'lino_voga.lib.voga.fixtures',
])

SETUP_INFO.update(message_extractors={
    'lino_voga': [
        ('**/cache/**', 'ignore', None),
        ('**.py', 'python', None),
        ('**.js', 'javascript', None),
        ('**.html', 'jinja2', None),
        ('**/config/**.html', 'jinja2', None),
        ('**/config/**/**.html', 'jinja2', None),
        ('lino_voga/lib/voga/config/courses/Enrolment/**.html',
         'jinja2', None),

    ],
})

SETUP_INFO.update(include_package_data=True)

# SETUP_INFO.update(package_data=dict())
#
#
# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l
#
#
# ~ add_package_data('lino_voga',
# ~ 'config/patrols/Patrol/*.odt',
# ~ 'config/patrols/Overview/*.odt')
# add_package_data('lino_voga.lib.voga', 'config/logo.jpg')
# add_package_data('lino_voga.lib.voga', 'config/courses/Course/*.*')
# add_package_data('lino_voga.lib.voga', 'config/courses/Enrolment/*.*')
# add_package_data('lino_voga.lib.voga', 'config/courses/Topic/*.*')
# add_package_data('lino_voga.lib.voga', 'config/excerpts/*.*')
# add_package_data('lino_voga.lib.voga', 'config/sales/Invoice/*.*')
#
# l = add_package_data('lino_voga')
# for lng in 'de fr'.split():
#     l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
