

# pip
# http://www.pip-installer.org/en/latest/requirements.html
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
