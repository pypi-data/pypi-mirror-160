import setuptools
with open(r'C:\Users\Claus X\Desktop\README_Ru.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='Cyberdisnake',
	version='1.0.0',
	author='NikaDevil',
	author_email='ply123123q@gmail.com',
	description='Страницы по рекции disnake',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['Cybernator_disnake'],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)