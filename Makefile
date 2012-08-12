SHELL=/bin/bash

init:
	sudo rm -rf bundle/
	mkdir -p bundle
	rm pacman.txt
	rm yaourt.txt
	rm pip-requirements.txt
	rm pip-requirements_sudo.txt

#
# pip # http://www.pip-installer.org/en/latest/requirements.html
#
backup_pip:
	sudo pip freeze > pip-requirements_sudo.txt
	pip freeze > pip-requirements.txt
restore_pip:
	sudo pip install -r pip-requirements_sudo.txt
	pip install --user -r pip-requirements.txt
upgrade_pip:
	sudo pip install --upgrade -r pip-requirements_sudo.txt
	pip install --user --upgrade -r pip-requirements.txt
	@echo suggest to run `make backup_pip` after a upgrade

#
# arch_conf
#

backup_arch_conf:
	python arch_conf.py -b filelist.txt
	sudo python arch_conf.py -b filelist_sudo.txt

restore_arch_conf:
	python arch_conf.py -r filelist.txt
	sudo python arch_conf.py -r filelist_sudo.txt

#
# package : pacman + yaourt
#
backup_package:
	comm -23 <(pacman -Qeq|sort) <(pacman -Qmq|sort) > pacman.txt
	pacman -Qmq | sort > yaourt.txt

restore_package:
	sudo pacman -S --needed $$(< pacman.txt)
	# TODO if 0 package need to be install
	yaourt -S yaourt $(shell comm -23 yaourt.txt <(yaourt -Qmq|sort))

backup: backup_pip backup_arch_conf backup_package
	@backup done,you can `git commit` if you\'d like to use this repo as a backup media
restore: restore_package restore_arch_conf restore_pip
	@restore done
