from setuptools import setup, find_packages

setup(
    name='personal-assistant',
    version='1.0.0',
    author='Vadym Mykhailiukov&Team#10',
    author_email='vidam1973@ukr.net',
    description='Персональний помічник для управління контактами, нотатками та файлами.',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Список залежностей, якщо вони є. Наприклад:
        # 'requests',
    ],
    entry_points={
        'console_scripts': [
            'personal-assistant=main:main',  # Точка входу до вашої програми
        ],
    },
)

