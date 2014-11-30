export PYTHONPATH := $(CURDIR):$(CURDIR)/tests
export DJANGO_SETTINGS_MODULE := django_settings

messages:
	cd cmsplugin_articles && django-admin.py makemessages -l en

compile:
	cd cmsplugin_articles && django-admin.py compilemessages
