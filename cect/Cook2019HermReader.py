# Reader for Cook et al 2019 data


from cect.Cook2019DataReader import Cook2019DataReader
from cect.ConnectomeReader import analyse_connections

import sys


def get_instance():
    return Cook2019DataReader("Hermaphodite")


my_instance = get_instance()

read_data = my_instance.read_data
read_muscle_data = my_instance.read_muscle_data

READER_DESCRIPTION = (
    """Data extracted from **%s** for neuronal connectivity"""
    % my_instance.filename.split("/")[-1]
)


def main1():
    cells, neuron_conns = my_instance.read_data()
    neurons2muscles, muscles, muscle_conns = my_instance.read_muscle_data()
    analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns)

    if "-nogui" not in sys.argv:
        my_instance.connection_number_plot("Acetylcholine")


if __name__ == "__main__":
    main1()
