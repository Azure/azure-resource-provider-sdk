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

# dev settings
dev = {}
dev["connection_uri"] = "http://localhost:5000"

# database settings
database = {}
database["prod"] = {
						"user":"someuser",
						"password":"somepassword",
						"host":"somehost",
						"database":"somedatabase"
					}
database["test"] = {
						"user":"someuser",
						"password":"somepassword",
						"host":"somehost",
						"database":"somedatabase"
					}

# Fabric deployment settings
deployment = {}
deployment["localpath"] = "path to local code repo"
deployment["remotepath"] = "path to remote server directory"
deployment["host"] = "somehost"
deployment["user"] = "someuser"
deployment["password"] = "somepassword"