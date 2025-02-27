import json
import os

class ConfigFile:

    def __init__(self, filename, default):
        self.filename = filename
        self.default = default
        self.load()
        self.mtime = os.path.getmtime(self.filename)

    def load(self):
        self.config = self.default
        try:
            with open(self.filename) as f:
                self.config_ = json.load(f)
        except:
            self.config_ = {}
        # Update default values with values in config file.
        self.config.update(self.config_)
        # If they are different then save.  Note, this is mostly used when 
        # copying settings from another version.  We may had added config
        # options to the new version that will be in the default config, but 
        # not in the config that was copied over.  
        # And we can delete certain config values and they will be added back 
        # with the default value. 
        if self.config!=self.config_:
            self.save()

    # Check to see if file has changed and reload if it has.  Do nothing otherwise.
    def reload(self):
        mtime = os.path.getmtime(self.filename)
        if mtime!=self.mtime:
            self.load()
            self.mtime = mtime
            return True
        return False

    def save(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self.config, f)
        except Exception as e:
            print(f"Unable to write config file {self.filename}: {e}")

