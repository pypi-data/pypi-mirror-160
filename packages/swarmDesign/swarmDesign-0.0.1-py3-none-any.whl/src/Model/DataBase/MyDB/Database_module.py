import sqlite3
from src.Model.DataBase.MyDB.exceptions.DataBaseExceptions import SignUpError, SignInError


class DataBase:

    def __init__(self):
        self.connection = sqlite3.connect('data.db')
        self.c = self.connection.cursor()
        self.create_users_data_table()
        self.create_projects_table()
        self.create_cluster_connections_table()

    def create_users_data_table(self):
        table = 'CREATE TABLE IF NOT EXISTS usersdata(user_name TEXT UNIQUE, password TEXT, space TEXT)'
        self.c.execute(table)

    def create_projects_table(self):
        table = 'CREATE TABLE IF NOT EXISTS projects(user_name TEXT, project_name TEXT, path TEXT, on_cluster ' \
                'BOOLEAN, UNIQUE(user_name, project_name, on_cluster)) '
        self.c.execute(table)

    def create_cluster_connections_table(self):
        table = 'CREATE TABLE IF NOT EXISTS connections(path TEXT, host_name TEXT, ' \
                'cluster_username TEXT, password TEXT, ' \
                'UNIQUE(path))'
        self.c.execute(table)

    def add_user(self, user_name, password, space):
        values = (user_name, password, space)
        insert = 'INSERT INTO usersdata VALUES ' + str(values)
        try:
            self.c.execute(insert)
            self.connection.commit()
            print("User Added !")
        except sqlite3.IntegrityError:
            raise SignUpError('Username already exists')

    def show_all_user(self):
        self.c.execute('SELECT * FROM usersdata')
        data = self.c.fetchall()
        return data

    def show_all_projects(self):
        self.c.execute('SELECT * FROM projects')
        data = self.c.fetchall()
        return data

    def get_user_info(self, user_name, password):  # function does not do one thing !
        self.c.execute('SELECT * FROM usersdata WHERE user_name="' + user_name + '"')
        data = self.c.fetchall()
        if len(data) == 0:
            raise SignInError("User does not exist")
        if data[0][1] != password:
            raise SignInError("Wrong password")
        return data

    def add_project(self, user_name, project_name, directory, on_cluster):
        values = (user_name, project_name, directory, on_cluster)
        insert = 'INSERT INTO projects VALUES ' + str(values)
        try:
            self.c.execute(insert)
            self.connection.commit()
            print("Project Added !")
        except sqlite3.IntegrityError:
            raise SignUpError('Project already exists')

    def get_project(self, user_name, project_name):
        self.c.execute('SELECT * FROM projects WHERE user_name="' + user_name + '"' + ' and project_name="' +
                       project_name + '"')
        data = self.c.fetchall()
        if len(data) == 0:
            raise SignInError("Project not found")
        return data

    def add_cluster_access(self, path, hostname, cluster_username, password):
        values = (path, hostname, cluster_username, password)
        insert = 'INSERT INTO connections VALUES ' + str(values)
        self.c.execute(insert)
        self.connection.commit()
        print("Cluster connection saved!")

    def get_cluster_access(self, path):
        self.c.execute('SELECT * FROM connections WHERE path="' + path + '"')
        data = self.c.fetchall()
        if len(data) == 0:
            raise SignInError("Access to cluster not found")
        return data
