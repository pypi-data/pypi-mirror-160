from setuptools import setup, find_packages

setup(name='naver_translation', # 패키지 명

version='2.0.0',

description='네이버 API를 사용한 비공식 번역 라이브러리입니다.',

author='VoidAsMad',

author_email='voidasmad@gmail.com',

url='https://github.com/VoidAsMad/Naver_Translation',

license='MIT', # MIT에서 정한 표준 라이센스 따른다

py_modules=['random'], # 패키지에 포함되는 모듈

python_requires='>=3',

install_requires=[], # 패키지 사용을 위해 필요한 추가 설치 패키지

packages=['naver_translation'] # 패키지가 들어있는 폴더들

)