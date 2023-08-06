from src.Model.Entities.Environment.Installation.Repositories import *
from src.Model.Entities.Environment.Installation.Grammar.Grammar import Grammar
import subprocess
import os
import shutil
import glob
from paramiko import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import AuthenticationException
from src.Model.DataBase.MyDB.Database_module import DataBase
from src.Model.Entities.Environment.Installation.exceptions.ClusterExceptions import ClusterError

# import GitPython
Linux_script = "scripts/dependency/Linux_dependencies.sh"


class OperatingSystem:

    def __init__(self):
        self.type = self.get_os_type()
        if self.is_linux_operating_system():
            self.cluster = self.detect_cluster()
        else:
            print("Software not implemented for this OS : ", self.type)
            # exit()

    def get_os_type(self):
        # os = subprocess.run(["uname"], capture_output=True, text=True)
        # os = os.stdout
        # os = os[:-1]  # be aware os = "Linux/n"
        os = subprocess.check_output(["uname"])  # py old ver
        if 'Linux' in str(os):  # py old ver
            os = "Linux"
        return os

    def is_linux_operating_system(self):
        return self.type == "Linux"

    def detect_cluster(self):
        cluster = False
        # distributor_id = subprocess.run(["lsb_release", "-a"], capture_output=True, text=True)
        # distributor_id = distributor_id.stdout
        distributor_id = subprocess.check_output(["lsb_release", "-a"])  # py old ver
        if "CentOS" in str(distributor_id):  # CentOS
            cluster = True
        return cluster

    def is_cluster(self):
        return self.cluster


class Dependencies:
    """
    This class will check if the needed version of all the necessary packages are installed.
    If a package is missing it will first ask and then install it. Necessary packages are
    OS dependent.
    """

    def __init__(self, os):
        self.not_install_pckg = None
        self.OS = os
        # print(os)
        self.check_dependencies()

    def check_dependencies(self):
        if self.OS == 'Linux':
            # subprocess.run(['echo $PWD'], shell=True)
            # subprocess.run(['ls -a'], shell=True)
            packages = subprocess.run([Linux_script], capture_output=True, text=True)
            packages = packages.stdout
            packages = packages[:-1]
        else:
            print("Undefined os", self.OS)
            exit(0)
        print(packages)
        for i in range(len(packages) - 1, 0, -1):
            if packages[i] == ':':
                if i != len(packages) - 2:
                    self.not_install_pckg = packages[i + 3:]
                break
        if self.not_install_pckg is None:
            print("All package are installed")
        else:
            print("Install following packages : ", self.not_install_pckg)

    def check_Linux(self):
        pass

    def install_pckg(self):
        """
        Install the self.not_install_pckg !
        :return:
        """
        pass


class SetupEnv:
    """
    Installation of the environment (locally) at path
    """

    def __init__(self, path, operating_sys):
        self.current_working_dir = os.getcwd()
        #print("CWD = ", self.current_working_dir)
        self.ENV_PATH = path
        # print("env_path = ", self.ENV_PATH)
        # self.change_directory(self.ENV_PATH)
        self.operating_sys = operating_sys
        # self.initiate_env()

    def existing_directory(self, dir_name):
        """
        Check if a directory already exists
        :param dir_name: directory name (from the current working dir)
        :return: boolean ture if the dir exists otherwise false
        """
        return os.path.isdir(dir_name)

    def change_directory(self, directory):
        """
        Move to the current working directory to another directory
        :param directory: target directory
        """
        os.chdir(directory)

    def create_dir(self, dir_name):
        """
        Creating a new directory in the current working dir
        :param dir_name: name of the new directory
        """
        os.mkdir(dir_name)

    def create_project_dir(self, path, project_name):  # should call this fct when we know that we are creating a new P
        self.change_directory(path)
        if self.existing_directory(project_name):  # temporal if statement should be removed since we should already
            return os.path.join(path, project_name)  # know that there is no such a project
        os.mkdir(project_name)
        return os.path.join(path, project_name)

    def set_env_path(self, proj_dir):
        self.ENV_PATH = os.path.join(self.ENV_PATH, proj_dir)

    def initiate_env(self):
        """
        Initiate the environment by cloning, compiling and installing repos.
        Maybe I should first clone and then build and install! Rather than having function with     #remark !!
        3 parameters !
        """
        self.change_directory(self.ENV_PATH)
        if self.operating_sys.is_cluster():
            self.install_argos_for_cluster()
        else:
            self.install('argos3', ARGOS3_REPOSITORY, "scripts/installation/argos3.sh")
        self.remove_legacy_e_puck_lib()
        self.generate_argos3_installation_source_file()
        if self.operating_sys.is_cluster():
            self.install_epuck_libraries_for_cluster()
        else:
            self.install('argos3-epuck', EPUCK_LIBRARIES_REPOSITORY, "scripts/installation/e_puck.sh")
        self.install('demiurge-epuck-dao', DEMIURGE_EPUCK_DAO_REPOSITORY, "scripts/installation/dao.sh")
        self.install('argos3-arena', ARGOS3_ARENA_REPOSITORY, "scripts/installation/arena.sh")
        self.install('experiments-loop-functions', LOOP_FUNCTIONS_REPOSITORY, "scripts/installation"
                                                                             "/loop_functions.sh")
        self.install('Demiurge', DEMIURGE_REPOSITORY, "scripts/installation/demiurge.sh")
        self.generate_demiurge_config_file()
        self.install('irace_pckg', IRACE_2_2_REPOSITORY, "scripts/installation/irace.sh")
        self.generate_irace_installation_source_file()

    def remove_legacy_e_puck_lib(self):
        """
        Removes ths legacy e-puck libraries from the current argos3 distribution
        """
        shutil.rmtree("argos3-dist/include/argos3/plugins/robots/e-puck")
        files = glob.glob("argos3-dist/lib/argos3/lib*epuck*.so")  # gives you all the globed files in a list
        for file in files:
            os.remove(file)

    def clone_repo(self, repo, dir_name):
        """
        This function clone the given repository in the dir_name directory
        :param repo: repository HTTPS
        :param dir_name: target directory
        """
        # subprocess.run(['git', 'clone', repo, dir_name])
        subprocess.call(['git', 'clone', repo, dir_name])  # py old ver

    def install(self, dir_name, git_repo, script):
        """
        Install a git repository in a new folder called dir_name
        :param dir_name: The directory to install
        :param git_repo: The repository to clone
        :param script: the script to run in order to compile and/or  install
        """
        if not os.path.isdir(os.path.join(self.ENV_PATH, dir_name)):
            self.clone_repo(git_repo, dir_name)
            # subprocess.run([os.path.join(self.current_working_dir, script)])
            path = os.path.join(self.current_working_dir, 'src/Model/Entities/Environment/Installation')
            subprocess.call([os.path.join(path, script)])  # py old ver
        else:
            print("Already cloned and installed: ", dir_name)

    def install_argos_for_cluster(self):
        if not os.path.isdir(os.path.join(self.ENV_PATH, 'argos3')):  # temporal if statement
            self.clone_repo(ARGOS3_REPOSITORY, 'argos3')
            self.change_directory('argos3')
            # subprocess.run(['git', 'checkout', '3.0.0-beta48'])
            subprocess.call(['git', 'checkout', '3.0.0-beta48'])  # py old ver
            self.cmake_version_change()
            self.change_directory(self.ENV_PATH)
            # subprocess.run([os.path.join(self.current_working_dir, 'scripts/installation/argos3_for_cluster.sh')])
            subprocess.call([os.path.join(self.current_working_dir,
                                          'scripts/installation/argos3_for_cluster.sh')])  # py old ver
        else:
            print("Already cloned and installed: ", 'argos3')

    def cmake_version_change(self):
        # subprocess.run(['sed', '-i', 's/2.8.12/2.8.8/g', 'src/CMakeLists.txt'])
        subprocess.call(['sed', '-i', 's/2.8.12/2.8.8/g', 'src/CMakeLists.txt'])

    def install_epuck_libraries_for_cluster(self):
        if not os.path.isdir(os.path.join(self.ENV_PATH, 'argos3-epuck')):  # temporal if statement
            self.clone_repo(EPUCK_LIBRARIES_REPOSITORY, 'argos3-epuck')
            self.change_directory('argos3-epuck')
            # subprocess.run(['git', 'checkout', 'v48'])
            subprocess.call(['git', 'checkout', 'v48'])
            self.remove_e_puck_visualisation()
            self.change_directory(self.ENV_PATH)
            # subprocess.run([os.path.join(self.current_working_dir, 'scripts/installation/e_puck_for_cluster.sh')])
            subprocess.call([os.path.join(self.current_working_dir,
                                          'scripts/installation/e_puck_for_cluster.sh')])
        else:
            print("Already cloned and installed: ", 'argos3-epuck')

    def remove_e_puck_visualisation(self):
        file = "src/plugins/robots/e-puck/CMakeLists.txt"
        # subprocess.run(['sed', '-i', 's/include(VisionTools.cmake)/#include(VisionTools.cmake)/g', file])
        subprocess.call(['sed', '-i', 's/include(VisionTools.cmake)/#include(VisionTools.cmake)/g', file])

    def generate_argos3_installation_source_file(self):
        cmd = "#!/bin/bash" + '\n' + \
              "export PKG_CONFIG_PATH=" + self.ENV_PATH + "/argos3-dist/lib/pkgconfig" + '\n' + \
              "export ARGOS_PLUGIN_PATH=" + self.ENV_PATH + "/argos3-dist/lib/argos3" + '\n' + \
              "export LD_LIBRARY_PATH=$ARGOS_PLUGIN_PATH:$LD_LIBRARY_PATH" + '\n' + \
              "export PATH=" + self.ENV_PATH + "/argos3-dist/bin/:$PATH" + '\n' + \
              "export INSTALLATION_PATH=" + self.ENV_PATH + '\n'
        with open("export_argos3_path.sh", "w") as f:
            f.write(cmd)
        self.change_directory(self.ENV_PATH)

    def generate_irace_installation_source_file(self):
        cmd = "#!/bin/bash" + '\n' + \
              "export R_LIBS_USER=" + self.ENV_PATH + "/irace_pckg/R_LIBS_USER" + '\n' + \
              "export R_LIBS=${R_LIBS_USER}:${R_LIBS}" + '\n' + \
              "export IRACE_HOME=" + self.ENV_PATH + "/irace_pckg/R_LIBS_USER/irace" + '\n' + \
              "export PATH=${IRACE_HOME}/bin/:$PATH" + '\n'
        with open("export_irace_path.sh", "w") as f:
            f.write(cmd)
        self.change_directory(self.ENV_PATH)

    def generate_demiurge_config_file(self):
        """
        Creates a file HOME/.config/AutoMoDe_Harlequin.conf where the path to Demiurge is set.
        """
        demiurge_path = os.path.join(self.ENV_PATH, 'Demiurge')
        home_config_path = os.path.join(os.getenv('HOME'), ".config")
        self.change_directory(home_config_path)
        with open("AutoMoDe_Harlequin.conf", "w") as f:
            f.write(demiurge_path)
        self.change_directory(self.ENV_PATH)

    def install_editor(self):
        if not os.path.isdir(os.path.join(self.ENV_PATH, 'Visual_design_tool')):
            self.change_directory(self.ENV_PATH)
            self.install('Visual_design_tool', EDITOR_REPOSITORY, "scripts/installation/editor.sh")
            self.change_directory('Visual_design_tool')
            self.write_in_editor_env_file(self.get_editor_env_file_content())
            self.change_directory(self.ENV_PATH)
        else:
            print("Editor already installed")

    def get_editor_env_file_content(self):
        path_to_automode_executable = os.path.join(self.ENV_PATH, "Demiurge/bin/automode_main")
        path_to_argos_experiment_file = "/home/ammar/Desktop/experiment/demiurge_scenario.argos"  # should be a param
        info = "AUTOMODE_PATH=" + path_to_automode_executable + '\n' + "EXPERIMENT_PATH=" + \
               path_to_argos_experiment_file
        return info

    def write_in_editor_env_file(self, info):
        with open(".env", "w") as f:
            f.write(info)

    def run_editor(self):
        # subprocess.run([os.path.join(self.current_working_dir, 'scripts/run_editor.sh')])
        path = os.path.join(self.current_working_dir, 'src/Model/Entities/Environment')
        self.change_directory(self.ENV_PATH)
        subprocess.call([os.path.join(path, 'Simulation/scripts/run_editor.sh')])

    def add_missions(self, repository):
        self.change_directory(self.ENV_PATH)
        self.install("Missions", repository, "scripts/installation/missions.sh")

    def get_missions(self):
        self.change_directory(self.ENV_PATH)
        missions = subprocess.run(["find", "-L", "./Missions/", "-name", "*.xml"], capture_output=True, text=True)
        # print(missions.stderr)
        # print(missions.stdout) maybe check if mission folder does exist
        return missions.stdout.split()

    def set_mission(self, path_to_mission):
        self.set_mission_for_editor(path_to_mission)
        self.set_mission_for_design_process(path_to_mission)

    def set_mission_for_editor(self, path_to_mission):
        self.change_directory(os.path.join(self.ENV_PATH, "Visual_design_tool"))
        abs_path_to_mission = os.path.join(self.ENV_PATH, path_to_mission[2:])
        subprocess.run(['sed', '-i', '/EXPERIMENT_PATH/c\EXPERIMENT_PATH=' + abs_path_to_mission, '.env'])

    def set_mission_for_design_process(self, path_to_mission):
        print('setting mission for design process')
        self.change_directory(self.ENV_PATH)
        destination_path = 'Demiurge/optimization/example/experiments-folder/mission.argos'
        shutil.copyfile(path_to_mission[2:], destination_path)
        self.disable_visualization(destination_path)
        # maybe check library path and automode path

    def disable_visualization(self, path_to_mission_file):
        subprocess.run(['sed', '-i', 's/<qt-opengl>/<!-- <qt-opengl>/g', path_to_mission_file])
        subprocess.run(['sed', '-i', 's+</qt-opengl>+</qt-opengl> -->+g', path_to_mission_file])

    def generate_grammar(self, flags):
        target_dir = os.path.join(self.ENV_PATH, "Demiurge/optimization/example")
        self.change_directory(target_dir)
        Grammar(flags)
        self.change_directory(self.ENV_PATH)

    def run_irace(self):
        # need first to set the AUTOMODE_HARLEQUINE_FILE
        # subprocess.run([os.path.join(self.current_working_dir, 'scripts/run_irace.sh')])  # exp irace path from bashrc
        path = os.path.join(self.current_working_dir, 'src/Model/Entities/Environment')
        subprocess.call([os.path.join(path, 'Simulation/scripts/run_irace.sh')])

    def get_status(self):
        # get_RData
        pass


class ClusterEnv:
    """
        Installation of the environment on cluster at path
    """

    def __init__(self, path, operating_sys):

        self.ENV_PATH = path
        self.hostname, self.cluster_username, self.password = self.set_cluster_info()
        self.client = self.cluster_connection()

        self.current_working_dir = os.getcwd()
        self.operating_sys = operating_sys
        print(self.ENV_PATH)

    def cluster_connection(self):
        client = SSHClient()
        client.load_host_keys('/home/ammar/.ssh/known_hosts')  # should be a parameter   /Users/ammar/.ssh/known_hosts
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(self.hostname, username=self.cluster_username, password=self.password)
        return client

    def set_cluster_info(self):
        db = DataBase()
        info = db.get_cluster_access(self.ENV_PATH)[0]
        hostname = info[1]
        cluster_username = info[2]
        password = info[3]
        return hostname, cluster_username, password

    def initiate_env(self):
        self.run_cmd_on_cluster(self.install('argos3', ARGOS3_REPOSITORY, "scripts/installation/argos3_for_cluster.sh"))
        self.run_cmd_on_cluster(self.remove_legacy_e_puck_lib_cmd())
        self.run_cmd_on_cluster(self.generate_argos3_installation_source_cmd())
        self.run_cmd_on_cluster(self.install_epuck_libraries_for_cluster_cmd())
        self.run_cmd_on_cluster(self.install('demiurge-epuck-dao', DEMIURGE_EPUCK_DAO_REPOSITORY, "scripts/installation/dao.sh"))
        self.run_cmd_on_cluster(self.install('argos3-arena', ARGOS3_ARENA_REPOSITORY, "scripts/installation/arena.sh"))
        self.run_cmd_on_cluster(self.install('experiments-loop-functions', LOOP_FUNCTIONS_REPOSITORY
                                            , "scripts/installation/loop_functions.sh"))
        self.run_cmd_on_cluster(self.install('Demiurge', DEMIURGE_REPOSITORY, "scripts/installation/demiurge.sh"))
        self.run_cmd_on_cluster(self.generate_demiurge_config_file_cmd())
        self.install_Rmpi_for_irace_on_cluster()
        self.run_cmd_on_cluster(self.install("irace_pckg", IRACE_2_2_REPOSITORY, "scripts/installation/irace_on_cluster.sh"))
        self.run_cmd_on_cluster(self.generate_irace_installation_source_file())

    def change_directory(self, dir):
        cmd = 'cd ' + dir + '\n'
        return cmd

    def clone_repo(self, repo, dir_name):
        cmd = 'git clone ' + repo + ' ' + dir_name + '\n'
        return cmd

    def install(self, dir_name, git_repo, script):
        cmd = self.change_directory(self.ENV_PATH)
        cmd += self.clone_repo(git_repo, dir_name)
        cmd += self.run_script_on_cluster(script)
        return cmd

    def run_script_on_cluster(self, bash_path):
        cmd = "\n"
        path = os.path.join(self.current_working_dir, 'src/Model/Entities/Environment/Installation')
        with open(os.path.join(path, bash_path)) as fp:
            lines = fp.readlines()
        for line in lines:
            cmd += line
        return cmd

    def run_cmd_on_cluster(self, cmd):
        cmd = self.new_cluster_cmd(cmd)
        print(cmd)
        stdin, stdout, stderr = self.client.exec_command(cmd)
        if stdout.channel.recv_exit_status() == 0:
            output = f'STDOUT:\n{stdout.read().decode("utf8")}'
            # print(f'STDOUT: {stdout.read().decode("utf8")}')
            print(output)
            print('CMD done!')
            return output
        else:
            raise ClusterError(stderr.read().decode("utf8"))

    def not_bloking_cmd(self, cmd):
        cmd = self.new_cluster_cmd(cmd)
        transport = self.client.get_transport()
        channel = transport.open_session()
        channel.exec_command(cmd)

    def new_cluster_cmd(self, cmd):
        load_cmake = "module load cmake\n"
        first_old_then_new_cluster_cmd = "ssh newmajorana << " + "EOF\n" + load_cmake + cmd + "\nexit \nEOF\n"
        direct_new_cluster_cmd = load_cmake + cmd
        return direct_new_cluster_cmd

    def remove_legacy_e_puck_lib_cmd(self):
        cmd = ""
        cmd += self.change_directory(self.ENV_PATH)
        cmd += "rm -rf argos3-dist/include/argos3/plugins/robots/e-puck \n"
        cmd += "rm -rf argos3-dist/lib/argos3/lib*epuck*.so \n"
        return cmd

    def generate_argos3_installation_source_cmd(self):
        file_name = "export_argos3_path.sh"
        exp = "#!/bin/bash" + '\n' + \
              "export PKG_CONFIG_PATH=" + self.ENV_PATH + "/argos3-dist/lib/pkgconfig" + '\n' + \
              "export ARGOS_PLUGIN_PATH=" + self.ENV_PATH + "/argos3-dist/lib/argos3" + '\n' + \
              "export LD_LIBRARY_PATH=$ARGOS_PLUGIN_PATH:$LD_LIBRARY_PATH" + '\n' + \
              "export PATH=" + self.ENV_PATH + "/argos3-dist/bin/:$PATH" + '\n' + \
              "export INSTALLATION_PATH=" + self.ENV_PATH + '\n'
        cmd = self.change_directory(self.ENV_PATH)
        cmd += "echo -e '" + exp + "' > " + file_name
        return cmd

    def install_epuck_libraries_for_cluster_cmd(self):
        cmd = self.change_directory(self.ENV_PATH)
        cmd += self.clone_repo(EPUCK_LIBRARIES_REPOSITORY, 'argos3-epuck')
        cmd += self.change_directory('argos3-epuck')
        cmd += 'git checkout v48 \n'
        # removing visualisation for cluster
        file = "src/plugins/robots/e-puck/CMakeLists.txt"
        cmd += "sed -i s/include'('VisionTools.cmake')'/#include'('VisionTools.cmake')'/g " + file + ' \n'
        cmd += self.change_directory(self.ENV_PATH)
        cmd += self.run_script_on_cluster('scripts/installation/e_puck_for_cluster.sh')
        return cmd

    def generate_demiurge_config_file_cmd(self):
        """
        CMD to Creates a file HOME/.config/AutoMoDe_Harlequin.conf where the path to Demiurge is set.
        """
        demiurge_path = os.path.join(self.ENV_PATH, 'Demiurge')
        cmd = "mkdir .config \n"
        cmd += self.change_directory(".config")
        cmd += "echo " + demiurge_path + " > AutoMoDe_Harlequin.conf \n"
        return cmd

    def editor(self):
        pass

    def add_missions(self, repository):
        dir_name = "Missions"
        script = "scripts/installation/missions.sh"
        cmd = self.install(dir_name, repository, script)
        print(cmd)
        self.run_cmd_on_cluster(cmd)

    def get_missions(self):
        cmd = self.change_directory(self.ENV_PATH)
        cmd += "find -L ./Missions/ -name *.xml \n"
        out = self.run_cmd_on_cluster(cmd)
        out = out.split()[1:]
        return out
        # maybe check if mission folder does exist and index 1 of split exist

    def set_mission(self, path_to_mission):
        self.set_mission_for_design_process(path_to_mission)

    def set_mission_for_design_process(self, path_to_mission):
        print('setting mission for design process')
        cmd = self.change_directory(self.ENV_PATH)
        destination_path = 'Demiurge/optimization/example/experiments-folder/mission.argos'
        cmd += "cp " + path_to_mission[2:] + " " + destination_path + '\n'
        cmd += self.disable_visualization(destination_path)
        # maybe check library path and automode path
        self.run_cmd_on_cluster(cmd)

    def disable_visualization(self, path_to_mission_file):
        cmd = 'sed' + " " + '-i' + " " + "'s/<qt-opengl>/<!-- <qt-opengl>/g'" + " " + path_to_mission_file + '\n'
        cmd += 'sed' + " " + '-i' + " " + "'s+</qt-opengl>+</qt-opengl> -->+g'" + " " + path_to_mission_file + '\n'
        return cmd

    def install_Rmpi_for_irace_on_cluster(self):
        cmd = self.change_directory(self.ENV_PATH)
        cmd += self.run_script_on_cluster('scripts/installation/Rmpi_for_cluster.sh')
        self.run_cmd_on_cluster(cmd)

    def generate_irace_installation_source_file(self):
        file_name = "export_irace_path.sh"
        cmd = self.change_directory(self.ENV_PATH)
        exp = "#!/bin/bash" + '\n' + \
              "export R_LIBS_USER=" + self.ENV_PATH + "/R/library" + '\n' + \
              "export R_LIBS=${R_LIBS_USER}:${R_LIBS}" + '\n' + \
              "export IRACE_HOME=" + self.ENV_PATH + "/R/library/irace" + '\n' + \
              "export PATH=${IRACE_HOME}/bin/:$PATH" + '\n'
        cmd += "echo -e '" + exp + "' > " + file_name
        return cmd

    def generate_grammar(self, flags):
        target_dir = os.path.join(self.ENV_PATH, "Demiurge/optimization/example")
        cmd = self.change_directory(os.path.join(self.ENV_PATH, target_dir))
        grammar = self.get_grammar(flags)
        cmd += "echo '" + grammar + "' > new_grammar.txt \n"
        self.run_cmd_on_cluster(cmd)

    def get_grammar(self, flags):
        Grammar(flags)
        with open("new_grammar.txt", "r") as grammar_file:
            lines = grammar_file.readlines()
        grammar = ""
        for line in lines:
            grammar += line
        os.remove("new_grammar.txt")
        return grammar

    def run_irace(self):
        # need first to set the AUTOMODE_HARLEQUINE_FILE
        # subprocess.run([os.path.join(self.current_working_dir, 'scripts/run_irace.sh')])  # exp irace path from bashrc
        cmd = self.change_directory(self.ENV_PATH)
        path = os.path.join(self.current_working_dir, 'src/Model/Entities/Environment')
        cmd += self.run_script_on_cluster(os.path.join(path, 'Simulation/scripts/run_irace.sh'))
        #print(cmd)
        #self.run_cmd_on_cluster(cmd)
        self.not_bloking_cmd(cmd)

    def run_irace_in_parallel(self):     #, nbr_cpu_cores, rack):
        nbr_cpu_cores = 2
        rack = 6
        cmd = self.change_directory(self.ENV_PATH)
        cmd += "source export_argos3_path.sh\n"
        cmd += "source export_irace_path.sh\n"
        cmd += self.change_directory("Demiurge/optimization/example/")
        cmd += "cp /opt/ohpc/pub/examples/slurm/tune-mpi-slurm-newmajorana tune-mpi-slurm-newmajorana\n"
        cmd += "./tune-mpi-slurm-newmajorana \$IRACE_HOME/bin execution-folder --parallel " + str(nbr_cpu_cores) + \
               " --rack " + str(rack) + " --scenario scenario.txt"
        self.run_cmd_on_cluster(cmd)
        #print(cmd)
        pass

    def get_RData_file(self):
        ftp_client = self.client.open_sftp()
        file_location_on_cluster = self.ENV_PATH + "/Demiurge/optimization/example/execution-folder/irace.Rdata"
        local_file_path = "/Users/ammar/Desktop/Analysis_RData/cluster_irace.Rdata"
        ftp_client.get(file_location_on_cluster, local_file_path)
        ftp_client.close()

    def get_status(self):
        self.get_RData_file()   # handel the erro while file is not existing !
        # process it for status


class Environment:

    def __init__(self, path, on_cluster):
        self.os = OperatingSystem()
        # Dependencies(self.os.type)
        self.installation_path = path  # "/home/demiurgeTester/ammar/Software"  # "/home/ammar/Desktop/Software"
        self.on_cluster = on_cluster
        if on_cluster:
            self.env = ClusterEnv(path, self.os)
        else:
            self.env = SetupEnv(path, self.os)

    def init_env(self):
        self.env.initiate_env()

    def install_editor(self):
        self.env.install_editor()

    def single_exp(self):
        self.env.run_editor()

    def add_missions(self, repo):
        self.env.add_missions(repo)

    def get_missions(self):
        missions = self.env.get_missions()
        return missions

    def set_mission(self, path_to_mission):
        self.env.set_mission(path_to_mission)

    def run_design_process(self, flags):
        self.generate_grammar(flags)
        self.env.run_irace()

    def run_design_process_in_parallel(self):
        self.env.run_irace_in_parallel()

    def generate_grammar(self, flags):
        self.env.generate_grammar(flags)

    def get_status(self):
        self.env.get_status()


if __name__ == "__main__":

    env = SetupEnv("/home/ammar/Desktop", OperatingSystem())
    env.install('irace_pckg', IRACE_2_2_REPOSITORY, "scripts/installation/irace.sh")
