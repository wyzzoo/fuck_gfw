# -*- coding: utf-8 -*-

# import pdb
import os
import sys
import shutil
import platform
from configparser import ConfigParser


plat = platform.platform().lower()

def change_pip_source(url='https://pypi.tuna.tsinghua.edu.cn/simple'):
	config_path = None
	if 'windows' in plat:
		config_path = os.path.expandvars('%userprofile%\\pip\\pip.ini')
	elif 'linux' in plat:
		config_path = '~/.pip/pip.conf'
	else:
		print('platform {} not support'.format(plat))
		return

	if os.path.exists(config_path):
		# 已经存在配置文件 备份一下
		bak_path = config_path + '.bak'
		if os.path.exists(bak_path):
			os.remove(bak_path)
		shutil.copy(config_path, target)
	else:
		# 有的时候连文件夹都没有 创建一下
		os.makedirs(os.path.dirname(config_path), exist_ok=True)

	conf = ConfigParser()
	conf.read(config_path)
	if 'global' not in conf:
		conf['global'] = {}
	conf['global']['index-url'] = url
	with open(config_path, 'w') as f:
		conf.write(f)

	print("[+] modify config succeeded")


def change_apt_source():
	if 'ubuntu' in plat:
		os.system("sudo sed -i 's/archive.ubuntu.com/mirrors.ustc.du.cn/g' /etc/apt/sources.list")
	elif 'kali' in plat:
		f = open('/etc/apt/sources.list', 'r')
		old = f.read()
		f.close()
		f = open('/etc/apt/sources.list', 'w')
		new = ''.join('deb https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib\n', 
					  'deb-src https://mirrors.ustc.edu.cn/kali kali-rolling main non-free contrib\n',
					  '\n',
					  old)
		f.write(new)
		f.close()
	else:
		print('[-] platform {} not supported!'.format(plat))
		return
	os.system("sudo apt update")


def main():
	change_pip_source()


if __name__ == '__main__':
	main()
	