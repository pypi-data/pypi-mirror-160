from src.Model.Entities.Environment.Installation.Execution_Unit import OperatingSystem
from src.Model.Entities.Environment.Installation.Execution_Unit import SetupEnv
from src.Model.Entities.Environment.Installation.Execution_Unit import Experiment

if __name__ == '__main__':
    ####
    # testing cluster version
    #subprocess.call(["ls", "-a"])
    #subprocess.call(["/home/ammar/PycharmProjects/AutoMoDeFw/src/scripts/cluster_version.sh"])
    #naa = subprocess.check_output(["lsb_release", "-a"])
    #print(naa)
    #exit()
    ####

    os = OperatingSystem()   # create the object somewhere else
    # print(os.type)
    # print(os.is_cluster)
    ########################################
    # checking the dependencies + Installing
    # Dependencies(os.type)

    ########################################
    # Setup the environment
    PATH = "/home/demiurgeTester/ammar/Software"    # "/home/ammar/Desktop/Software"
    env = SetupEnv(PATH, os)
    # env.install_editor()

    ########################################
    exp = Experiment(env)

    # run Experiment
    # exp.single_exp()

    # run Design process on localhost
    # need first to check if the Irace pkg is installed ! +  R installation -> bashrc file (see for local installation)
    exp.run_design_process()

