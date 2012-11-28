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