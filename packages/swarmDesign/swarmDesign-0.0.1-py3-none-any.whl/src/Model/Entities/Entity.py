from src.Model.Entities.Environment.Installation.Execution_Unit import Environment


class User:

    def __init__(self, user_name, password, user_space=None):
        self.name = user_name
        self.space = user_space
        self.password = password      # see later if needed

    def get_name(self):
        return self.name

    def get_space(self):
        return self.space

    def get_password(self):
        return self.password


class Project:

    def __init__(self, user_name, project_name, path, on_cluster):
        self.owner = user_name
        self.name = project_name
        self.location_path = path
        self.environment = Environment(self.location_path, on_cluster)
        self.on_cluster = on_cluster

    def get_project_name(self):
        return self.name

    def get_environment(self):
        return self.environment

    def init_env(self):
        self.environment.init_env()

    def is_on_cluster(self):
        return self.on_cluster
