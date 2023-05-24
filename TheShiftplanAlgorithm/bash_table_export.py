import sys 
import os

paths = {
    "cmd_out": ".",
    "manage_py": "../TheShiftplan/manage.py",
    "json_out": "_json"
}



class DefinePathError(Exception):
    """Exception raised if path does not exist and user doesnt want the program to create it.

    Attributes:
        path -- non existing path which caused the error
        message -- explanation of the error
    """

    def __init__(self, path, purpose):
        self.path = path
        self.message = "Please change {}_path: {}".format(purpose, self.path)
        super().__init__(self.message)

def check_or_build_path(path, purpose):
    if not os.path.exists(path):
        create = input("Path does not exisist. Create path {}? [[y]|n]".format(path))
        if create.lower().strip() != 'n':
            os.makedirs(path)
        else:
            raise DefinePathError(path, purpose)

for path in paths:
    check_or_build_path(paths[path], path)



defs_names = {
    "modes": "Mode",
    "shiftplans": "Shiftplan",
    "user_profiles": "UserProfile",
    "subcrews": "SubCrew", 
    "jobtypes": "Jobtype", 
    "jobs": "Job"
    }
defs_names = {n: "defs." + defs_names[n] for n in defs_names}

prefs_names = {
    "user_job_ratings": "UserJobRating",
    "user_options": "UserOptions",
    "bias_hours": "BiasHours"
    }
prefs_names = {n: "prefs.{}".format(prefs_names[n]) for n in prefs_names}

models_names = {
    "users": "auth.user",
    "groups": "auth.group"
    }
models_names.update(defs_names)
models_names.update(prefs_names)



def create_shell_dump_cmds(cmd_filename="_cmd_db_to_json.sh", models_names=models_names):
    base_str = "python {manage_py_path} dumpdata {what} > {filename}.json\n"
    cmd_str = ""
    for fn in models_names:
        fname = os.path.join(paths["json_out"], fn)
        cmd_str += base_str.format(manage_py_path=paths["manage_py"], what=models_names[fn], filename=fname)
    if cmd_filename:
        cmd_filename = os.path.join(paths["cmd_out"], cmd_filename)
        with open(cmd_filename, 'w') as f:
            f.write(cmd_str)
            print("New .sh file in: {}".format(cmd_filename))
    

if __name__ == "__main__":
    create_shell_dump_cmds()