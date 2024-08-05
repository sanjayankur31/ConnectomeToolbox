# -*- coding: utf-8 -*-

############################################################

#    Utilities for reading C. elegans connectome data

############################################################

import pandas as pd

SENSORY_NEURONS_COOK = [
    "ASIL",
    "ASIR",
    "ASJL",
    "ASJR",
    "AWAL",
    "AWAR",
    "ASGL",
    "ASGR",
    "AWBL",
    "AWBR",
    "ASEL",
    "ASER",
    "ADFL",
    "ADFR",
    "AFDL",
    "AFDR",
    "AWCL",
    "AWCR",
    "ASKL",
    "ASKR",
    "ASHL",
    "ASHR",
    "ADLL",
    "ADLR",
    "BAGL",
    "BAGR",
    "URXL",
    "URXR",
    "ALNL",
    "ALNR",
    "PLNL",
    "PLNR",
    "SDQL",
    "SDQR",
    "AQR",
    "PQR",
    "ALML",
    "ALMR",
    "AVM",
    "PVM",
    "PLML",
    "PLMR",
    "FLPL",
    "FLPR",
    "DVA",
    "PVDL",
    "PVDR",
    "ADEL",
    "ADER",
    "PDEL",
    "PDER",
    "PHAL",
    "PHAR",
    "PHBL",
    "PHBR",
    "PHCL",
    "PHCR",
    "IL2DL",
    "IL2DR",
    "IL2L",
    "IL2R",
    "IL2VL",
    "IL2VR",
    "CEPDL",
    "CEPDR",
    "CEPVL",
    "CEPVR",
    "URYDL",
    "URYDR",
    "URYVL",
    "URYVR",
    "OLLL",
    "OLLR",
    "OLQDL",
    "OLQDR",
    "OLQVL",
    "OLQVR",
    "IL1DL",
    "IL1DR",
    "IL1L",
    "IL1R",
    "IL1VL",
    "IL1VR",
]

INTERNEURONS_NONPHARYNGEAL_COOK = [
    "AINL",
    "AINR",
    "AIML",
    "AIMR",
    "RIH",
    "URBL",
    "URBR",
    "RIR",
    "AIYL",
    "AIYR",
    "AIAL",
    "AIAR",
    "AUAL",
    "AUAR",
    "AIZL",
    "AIZR",
    "RIS",
    "ALA",
    "PVQL",
    "PVQR",
    "ADAL",
    "ADAR",
    "RIFL",
    "RIFR",
    "BDUL",
    "BDUR",
    "PVR",
    "AVFL",
    "AVFR",
    "AVHL",
    "AVHR",
    "PVPL",
    "PVPR",
    "LUAL",
    "LUAR",
    "PVNL",
    "PVNR",
    "AVG",
    "DVB",
    "RIBL",
    "RIBR",
    "RIGL",
    "RIGR",
    "RMGL",
    "RMGR",
    "AIBL",
    "AIBR",
    "RICL",
    "RICR",
    "SAADL",
    "SAADR",
    "SAAVL",
    "SAAVR",
    "AVKL",
    "AVKR",
    "DVC",
    "AVJL",
    "AVJR",
    "PVT",
    "AVDL",
    "AVDR",
    "AVL",
    "PVWL",
    "PVWR",
    "RIAL",
    "RIAR",
    "RIML",
    "RIMR",
    "AVEL",
    "AVER",
    "RMFL",
    "RMFR",
    "RID",
    "AVBL",
    "AVBR",
    "AVAL",
    "AVAR",
    "PVCL",
    "PVCR",
    "RIPL",
    "RIPR",
]

HEAD_MOTORNEURONS_COOK = [
    "URADL",
    "URADR",
    "URAVL",
    "URAVR",
    "RMEL",
    "RMER",
    "RMED",
    "RMEV",
    "RMDDL",
    "RMDDR",
    "RMDL",
    "RMDR",
    "RMDVL",
    "RMDVR",
    "RIVL",
    "RIVR",
    "RMHL",
    "RMHR",
]

SUBLATERAL_MOTORNEURONS_COOK = [
    "SABD",
    "SABVL",
    "SABVR",
    "SMDDL",
    "SMDDR",
    "SMDVL",
    "SMDVR",
    "SMBDL",
    "SMBDR",
    "SMBVL",
    "SMBVR",
    "SIBDL",
    "SIBDR",
    "SIBVL",
    "SIBVR",
    "SIADL",
    "SIADR",
    "SIAVL",
    "SIAVR",
]

VENTRAL_CORD_MOTORNEURONS = [
    "DA1",
    "DA2",
    "DA3",
    "DA4",
    "DA5",
    "DA6",
    "DA7",
    "DA8",
    "DA9",
    "PDA",
    "DB1",
    "DB2",
    "DB3",
    "DB4",
    "DB5",
    "DB6",
    "DB7",
    "AS1",
    "AS2",
    "AS3",
    "AS4",
    "AS5",
    "AS6",
    "AS7",
    "AS8",
    "AS9",
    "AS10",
    "AS11",
    "PDB",
    "DD1",
    "DD2",
    "DD3",
    "DD4",
    "DD5",
    "DD6",
    "VA1",
    "VA2",
    "VA3",
    "VA4",
    "VA5",
    "VA6",
    "VA7",
    "VA8",
    "VA9",
    "VA10",
    "VA11",
    "VA12",
    "VB1",
    "VB2",
    "VB3",
    "VB4",
    "VB5",
    "VB6",
    "VB7",
    "VB8",
    "VB9",
    "VB10",
    "VB11",
    "VD1",
    "VD2",
    "VD3",
    "VD4",
    "VD5",
    "VD6",
    "VD7",
    "VD8",
    "VD9",
    "VD10",
    "VD11",
    "VD12",
    "VD13",
]

HERM_SPECIFIC_MOTORNEURONS = [
    "HSNL",
    "HSNR",
    "VC1",
    "VC2",
    "VC3",
    "VC4",
    "VC5",
    "VC6",
]

UNKNOWN_FUNCTION_NEURONS = ["CANL", "CANR"]


PHARANGEAL_MOTORNEURONS = [
    "M1",
    "M2L",
    "M2R",
    "M3L",
    "M3R",
    "M4",
    "M5",
]

PHARANGEAL_INTERNEURONS = [
    "I1L",
    "I1R",
    "I2L",
    "I2R",
    "I3",
    "I4",
    "I5",
    "I6",
]

PHARANGEAL_POLYMODAL_NEURONS = [
    "MI",
    "NSML",
    "NSMR",
    "MCL",
    "MCR",
]

INTERNEURONS_COOK = INTERNEURONS_NONPHARYNGEAL_COOK + PHARANGEAL_INTERNEURONS

PHARANGEAL_NEURONS = (
    PHARANGEAL_INTERNEURONS + PHARANGEAL_MOTORNEURONS + PHARANGEAL_POLYMODAL_NEURONS
)

MOTORNEURONS_COOK = (
    HEAD_MOTORNEURONS_COOK
    + SUBLATERAL_MOTORNEURONS_COOK
    + VENTRAL_CORD_MOTORNEURONS
    + PHARANGEAL_MOTORNEURONS
    + HERM_SPECIFIC_MOTORNEURONS
)

PREFERRED_NEURON_NAMES_COOK = (
    INTERNEURONS_COOK
    + SENSORY_NEURONS_COOK
    + MOTORNEURONS_COOK
    + PHARANGEAL_POLYMODAL_NEURONS
    + UNKNOWN_FUNCTION_NEURONS
)


PREFERRED_NEURON_NAMES = [
    "ADAL",
    "ADAR",
    "ADEL",
    "ADER",
    "ADFL",
    "ADFR",
    "ADLL",
    "ADLR",
    "AFDL",
    "AFDR",
    "AIAL",
    "AIAR",
    "AIBL",
    "AIBR",
    "AIML",
    "AIMR",
    "AINL",
    "AINR",
    "AIYL",
    "AIYR",
    "AIZL",
    "AIZR",
    "ALA",
    "ALML",
    "ALMR",
    "ALNL",
    "ALNR",
    "AQR",
    "AS1",
    "AS10",
    "AS11",
    "AS2",
    "AS3",
    "AS4",
    "AS5",
    "AS6",
    "AS7",
    "AS8",
    "AS9",
    "ASEL",
    "ASER",
    "ASGL",
    "ASGR",
    "ASHL",
    "ASHR",
    "ASIL",
    "ASIR",
    "ASJL",
    "ASJR",
    "ASKL",
    "ASKR",
    "AUAL",
    "AUAR",
    "AVAL",
    "AVAR",
    "AVBL",
    "AVBR",
    "AVDL",
    "AVDR",
    "AVEL",
    "AVER",
    "AVFL",
    "AVFR",
    "AVG",
    "AVHL",
    "AVHR",
    "AVJL",
    "AVJR",
    "AVKL",
    "AVKR",
    "AVL",
    "AVM",
    "AWAL",
    "AWAR",
    "AWBL",
    "AWBR",
    "AWCL",
    "AWCR",
    "BAGL",
    "BAGR",
    "BDUL",
    "BDUR",
    "CANL",
    "CANR",
    "CEPDL",
    "CEPDR",
    "CEPVL",
    "CEPVR",
    "DA1",
    "DA2",
    "DA3",
    "DA4",
    "DA5",
    "DA6",
    "DA7",
    "DA8",
    "DA9",
    "DB1",
    "DB2",
    "DB3",
    "DB4",
    "DB5",
    "DB6",
    "DB7",
    "DD1",
    "DD2",
    "DD3",
    "DD4",
    "DD5",
    "DD6",
    "DVA",
    "DVB",
    "DVC",
    "FLPL",
    "FLPR",
    "HSNL",
    "HSNR",
    "I1L",
    "I1R",
    "I2L",
    "I2R",
    "I3",
    "I4",
    "I5",
    "I6",
    "IL1DL",
    "IL1DR",
    "IL1L",
    "IL1R",
    "IL1VL",
    "IL1VR",
    "IL2DL",
    "IL2DR",
    "IL2L",
    "IL2R",
    "IL2VL",
    "IL2VR",
    "LUAL",
    "LUAR",
    "M1",
    "M2L",
    "M2R",
    "M3L",
    "M3R",
    "M4",
    "M5",
    "MCL",
    "MCR",
    "MI",
    "NSML",
    "NSMR",
    "OLLL",
    "OLLR",
    "OLQDL",
    "OLQDR",
    "OLQVL",
    "OLQVR",
    "PDA",
    "PDB",
    "PDEL",
    "PDER",
    "PHAL",
    "PHAR",
    "PHBL",
    "PHBR",
    "PHCL",
    "PHCR",
    "PLML",
    "PLMR",
    "PLNL",
    "PLNR",
    "PQR",
    "PVCL",
    "PVCR",
    "PVDL",
    "PVDR",
    "PVM",
    "PVNL",
    "PVNR",
    "PVPL",
    "PVPR",
    "PVQL",
    "PVQR",
    "PVR",
    "PVT",
    "PVWL",
    "PVWR",
    "RIAL",
    "RIAR",
    "RIBL",
    "RIBR",
    "RICL",
    "RICR",
    "RID",
    "RIFL",
    "RIFR",
    "RIGL",
    "RIGR",
    "RIH",
    "RIML",
    "RIMR",
    "RIPL",
    "RIPR",
    "RIR",
    "RIS",
    "RIVL",
    "RIVR",
    "RMDDL",
    "RMDDR",
    "RMDL",
    "RMDR",
    "RMDVL",
    "RMDVR",
    "RMED",
    "RMEL",
    "RMER",
    "RMEV",
    "RMFL",
    "RMFR",
    "RMGL",
    "RMGR",
    "RMHL",
    "RMHR",
    "SAADL",
    "SAADR",
    "SAAVL",
    "SAAVR",
    "SABD",
    "SABVL",
    "SABVR",
    "SDQL",
    "SDQR",
    "SIADL",
    "SIADR",
    "SIAVL",
    "SIAVR",
    "SIBDL",
    "SIBDR",
    "SIBVL",
    "SIBVR",
    "SMBDL",
    "SMBDR",
    "SMBVL",
    "SMBVR",
    "SMDDL",
    "SMDDR",
    "SMDVL",
    "SMDVR",
    "URADL",
    "URADR",
    "URAVL",
    "URAVR",
    "URBL",
    "URBR",
    "URXL",
    "URXR",
    "URYDL",
    "URYDR",
    "URYVL",
    "URYVR",
    "VA1",
    "VA10",
    "VA11",
    "VA12",
    "VA2",
    "VA3",
    "VA4",
    "VA5",
    "VA6",
    "VA7",
    "VA8",
    "VA9",
    "VB1",
    "VB10",
    "VB11",
    "VB2",
    "VB3",
    "VB4",
    "VB5",
    "VB6",
    "VB7",
    "VB8",
    "VB9",
    "VC1",
    "VC2",
    "VC3",
    "VC4",
    "VC5",
    "VC6",
    "VD1",
    "VD10",
    "VD11",
    "VD12",
    "VD13",
    "VD2",
    "VD3",
    "VD4",
    "VD5",
    "VD6",
    "VD7",
    "VD8",
    "VD9",
]

for n in PREFERRED_NEURON_NAMES:
    assert n in PREFERRED_NEURON_NAMES_COOK
for n in PREFERRED_NEURON_NAMES_COOK:
    assert n in PREFERRED_NEURON_NAMES

assert len(PREFERRED_NEURON_NAMES_COOK) == len(PREFERRED_NEURON_NAMES)

BODY_WALL_MUSCLE_NAMES = [
    "MDL01",
    "MDL02",
    "MDL03",
    "MDL04",
    "MDL05",
    "MDL06",
    "MDL07",
    "MDL08",
    "MDL09",
    "MDL10",
    "MDL11",
    "MDL12",
    "MDL13",
    "MDL14",
    "MDL15",
    "MDL16",
    "MDL17",
    "MDL18",
    "MDL19",
    "MDL20",
    "MDL21",
    "MDL22",
    "MDL23",
    "MDL24",
    "MDR01",
    "MDR02",
    "MDR03",
    "MDR04",
    "MDR05",
    "MDR06",
    "MDR07",
    "MDR08",
    "MDR09",
    "MDR10",
    "MDR11",
    "MDR12",
    "MDR13",
    "MDR14",
    "MDR15",
    "MDR16",
    "MDR17",
    "MDR18",
    "MDR19",
    "MDR20",
    "MDR21",
    "MDR22",
    "MDR23",
    "MDR24",
    "MVL01",
    "MVL02",
    "MVL03",
    "MVL04",
    "MVL05",
    "MVL06",
    "MVL07",
    "MVL08",
    "MVL09",
    "MVL10",
    "MVL11",
    "MVL12",
    "MVL13",
    "MVL14",
    "MVL15",
    "MVL16",
    "MVL17",
    "MVL18",
    "MVL19",
    "MVL20",
    "MVL21",
    "MVL22",
    "MVL23",
    "MVR01",
    "MVR02",
    "MVR03",
    "MVR04",
    "MVR05",
    "MVR06",
    "MVR07",
    "MVR08",
    "MVR09",
    "MVR10",
    "MVR11",
    "MVR12",
    "MVR13",
    "MVR14",
    "MVR15",
    "MVR16",
    "MVR17",
    "MVR18",
    "MVR19",
    "MVR20",
    "MVR21",
    "MVR22",
    "MVR23",
    "MVR24",
]


ANAL_MUSCLE_NAMES = ["MANAL"]

VULVAL_MUSCLE_NAMES = [
    "MVULVA",
    "vm1AL",
    "vm1PL",
    "vm1PR",
    "vm1AR",
    "vm2AL",
    "vm2AR",
    "vm2PL",
    "vm2PR",
]

ODD_PHARANGEAL_MUSCLE_NAMES = [
    "pm1",
    "pm3D",
    "pm3VL",
    "pm3VR",
    "pm5D",
    "pm5VR",
    "pm5VL",
    "pm7D",
    "pm7VL",
    "pm7VR",
]

EVEN_PHARANGEAL_MUSCLE_NAMES = [
    "pm2D",
    "pm2VL",
    "pm2VR",
    "pm4D",
    "pm4VR",
    "pm4VL",
    "pm6D",
    "pm6VR",
    "pm6VL",
    "pm8",
]

PHARANGEAL_MUSCLE_NAMES = ODD_PHARANGEAL_MUSCLE_NAMES + EVEN_PHARANGEAL_MUSCLE_NAMES


PREFERRED_MUSCLE_NAMES = (
    BODY_WALL_MUSCLE_NAMES
    + PHARANGEAL_MUSCLE_NAMES
    + VULVAL_MUSCLE_NAMES
    + ANAL_MUSCLE_NAMES
)

GLR_CELLS = [
    "GLRDL",
    "GLRDR",
    "GLRL",
    "GLRR",
    "GLRVL",
    "GLRVR",
]

KNOWN_OTHER_CELLS_COOK_19 = [
    "CEPshDL",
    "CEPshDR",
    "CEPshVL",
    "CEPshVR",
    "bm",
    "e2D",
    "e2VL",
    "e2VR",
    "e3D",
    "e3VL",
    "e3VR",
    "exc_cell",
    "exc_gl",
    "g1AL",
    "g1AR",
    "g1p",
    "g2L",
    "g2R",
    "hmc",
    "hyp",
    "int",
    "mc1DL",
    "mc1DR",
    "mc1V",
    "mc2DL",
    "mc2DR",
    "mc2V",
    "mc3DL",
    "mc3DR",
    "mc3V",
    "mu_anal",
    "mu_intL",
    "mu_intR",
    "mu_sph",
] + GLR_CELLS

KNOWN_OTHER_CELLS_COOK_20 = [
    "bm",
    "e2DL",
    "e2DR",
    "e2V",
    "e3D",
    "e3VL",
    "e3VR",
    "g1AL",
    "g1AR",
    "g1P",
    "g2L",
    "g2R",
    "mc2DL",
    "mc2DR",
    "mc2V",
    "mc2dl",
    "mc2dr",
    "mc3V",
]

KNOWN_OTHER_CELLS = KNOWN_OTHER_CELLS_COOK_19

for cell in KNOWN_OTHER_CELLS_COOK_20:
    if not cell in KNOWN_OTHER_CELLS:
        KNOWN_OTHER_CELLS.append(cell)


def get_standard_color(cell):
    from cect.WormAtlasInfo import WA_COLORS

    if cell in BODY_WALL_MUSCLE_NAMES:
        return WA_COLORS["Hermaphrodite"]["Muscle"]["body wall muscle"]
    elif cell in VULVAL_MUSCLE_NAMES:
        return WA_COLORS["Hermaphrodite"]["Muscle"]["vulval muscle"]
    elif cell in ODD_PHARANGEAL_MUSCLE_NAMES:
        return WA_COLORS["Hermaphrodite"]["Muscle"]["odd numbered pharyngeal muscle"]
    elif cell in EVEN_PHARANGEAL_MUSCLE_NAMES:
        return WA_COLORS["Hermaphrodite"]["Muscle"]["even numbered pharyngeal muscle"]
    elif cell in INTERNEURONS_COOK:
        return WA_COLORS["Hermaphrodite"]["Nervous Tissue"]["interneuron"]
    elif cell in SENSORY_NEURONS_COOK:
        return WA_COLORS["Hermaphrodite"]["Nervous Tissue"]["sensory neuron"]
    elif cell in MOTORNEURONS_COOK:
        return WA_COLORS["Hermaphrodite"]["Nervous Tissue"]["motor neuron"]
    elif cell in PHARANGEAL_POLYMODAL_NEURONS:
        return WA_COLORS["Hermaphrodite"]["Nervous Tissue"]["polymodal neuron"]
    elif cell in GLR_CELLS:
        return WA_COLORS["Hermaphrodite"]["Other Tissues"]["glr cell"]
    else:
        return "#dddddd"


def get_short_description(cell):
    if cell in BODY_WALL_MUSCLE_NAMES:
        return "Body wall muscle"
    elif cell in VULVAL_MUSCLE_NAMES:
        return "Vulval muscle"
    elif cell in ODD_PHARANGEAL_MUSCLE_NAMES or cell in EVEN_PHARANGEAL_MUSCLE_NAMES:
        return "Pharyngeal muscle"
    elif cell in PHARANGEAL_INTERNEURONS:
        return "Pharyngeal interneuron"
    elif cell in PHARANGEAL_MOTORNEURONS:
        return "Pharyngeal motor neuron"
    elif cell in PHARANGEAL_POLYMODAL_NEURONS:
        return "Pharyngeal polymodal neuron"
    elif cell in HERM_SPECIFIC_MOTORNEURONS:
        return "Hermaphrodite specific motor neuron"
    elif cell in INTERNEURONS_NONPHARYNGEAL_COOK:
        return "Interneuron"
    elif cell in SENSORY_NEURONS_COOK:
        return "Sensory neuron"
    elif cell in MOTORNEURONS_COOK:
        return "Motor neuron"
    elif cell in GLR_CELLS:
        return "GLR cell"
    else:
        return "???"


def get_cell_link(cell_name, html=False):
    url = None

    known_indiv = ["SABD", "MI"]

    if cell_name in known_indiv:
        url = (
            "https://www.wormatlas.org/neurons/Individual Neurons/%sframeset.html"
            % cell_name
        )
    elif cell_name[-2:].isnumeric():
        url = (
            "https://www.wormatlas.org/neurons/Individual Neurons/%sframeset.html"
            % cell_name[:-2]
        )
    elif cell_name[-1].isdigit():
        url = (
            "https://www.wormatlas.org/neurons/Individual Neurons/%sframeset.html"
            % cell_name[:-1]
        )
    elif (
        cell_name.endswith("L")
        or cell_name.endswith("R")
        or cell_name.endswith("EV")
        or cell_name.endswith("ED")
        or cell_name.endswith("BD")
    ):
        url = (
            "https://www.wormatlas.org/neurons/Individual Neurons/%sframeset.html"
            % cell_name[:-1]
        )
    elif len(cell_name) == 3:
        url = (
            "https://www.wormatlas.org/neurons/Individual Neurons/%sframeset.html"
            % cell_name
        )

    if url is not None:
        if html:
            return '<a href="%s">%s</a>' % (url, cell_name)
        else:
            return "[%s](%s)" % (cell_name, url)
    else:
        return cell_name


def _generate_cell_table(cells):
    all_data = {}

    all_data[""] = ["Link"]

    for cell in sorted(cells):
        all_data[cell] = [get_cell_link(cell)]

    df_all = pd.DataFrame(all_data).transpose()

    mk = df_all.to_markdown()

    return "%s\n\n" % mk


if __name__ == "__main__":
    from cect.WormAtlasInfo import WA_COLORS

    filename = "docs/Cells.md"

    with open(filename, "w") as f:
        for sex in WA_COLORS:
            f.write("\n## %s\n" % sex)

            for cell_class in WA_COLORS[sex]:
                f.write("\n### %s\n\n" % cell_class)

                for cell_type in WA_COLORS[sex][cell_class]:
                    if not "General code" in cell_type:
                        color = WA_COLORS[sex][cell_class][cell_type][1:]
                        f.write(
                            "#### ![#{0}](https://via.placeholder.com/15/{0}/{0}.png) {1}\n".format(
                                color, cell_type[0].upper() + cell_type[1:]
                            )
                        )
                        if cell_type == "body wall muscle":
                            f.write(_generate_cell_table(BODY_WALL_MUSCLE_NAMES))
                        elif cell_type == "interneuron":
                            f.write(_generate_cell_table(INTERNEURONS_COOK))
                        elif cell_type == "motor neuron":
                            f.write(_generate_cell_table(MOTORNEURONS_COOK))
                        elif cell_type == "sensory neuron":
                            f.write(_generate_cell_table(SENSORY_NEURONS_COOK))
                        elif cell_type == "neuron with unknown function":
                            f.write(_generate_cell_table(UNKNOWN_FUNCTION_NEURONS))
