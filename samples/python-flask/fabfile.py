#
# Copyright 2011 Microsoft Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from fabric.api import *
from resourceprovider import settings

# the user to use for the remote commands
env.user = settings.deployment["user"]
env.password = settings.deployment["password"]
# the servers where the commands are executed
env.hosts = [settings.deployment["host"]]

def _reload():
	sudo("service uwsgi restart")
	sudo("service nginx restart")

def _copy():
	put(settings.deployment["localpath"], settings.deployment["remotepath"])	

def _delete_local_extra_files():
	local("find . -name \*.pyc -delete")
	local("find . -name \.DS_Store -delete")

def deploy():
	_delete_local_extra_files()
	_copy()
	_reload()