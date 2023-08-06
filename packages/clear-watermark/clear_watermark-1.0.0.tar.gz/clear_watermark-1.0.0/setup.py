from setuptools import setup, find_packages

# with open('./requirements.txt') as f:
# 	requirements = f.readlines()

requirements = ['Pillow >= 7.2.0',]

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
		name ='clear_watermark',
		version ='1.0.0',
		author ='carlosmperilla',
		author_email ='carlosperillaprogramacion@gmail.com',
		url ='https://github.com/carlosmperilla/clear-watermark',
		description ='It uses OOP to insert one image as a watermark on other image.',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(where="."),
        include_package_data=True,
        package_data= {},
		entry_points ={},
		classifiers =[
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
        ],
		keywords ='watermark image branding mark editions edition package carlosmperilla',
		install_requires = requirements,
		zip_safe = False
)

print(find_packages(where="."))
