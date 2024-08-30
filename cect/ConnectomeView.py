from cect.Cells import PHARYNGEAL_NEURONS
from cect.Cells import PREFERRED_NEURON_NAMES
from cect.Cells import PREFERRED_MUSCLE_NAMES
from cect.Cells import KNOWN_OTHER_CELLS
from cect.Cells import SENSORY_NEURONS_COOK

from cect.Cells import SENSORY_NEURONS_COOK_CATEGORIES
from cect.Cells import INTERNEURONS_NONPHARYNGEAL_COOK_CATEGORIES

from cect.Cells import BODY_MUSCLES_COOK
from cect.Cells import HEAD_MUSCLES_COOK
from cect.Cells import HEAD_MOTORNEURONS_COOK
from cect.Cells import SUBLATERAL_MOTORNEURONS_COOK
from cect.Cells import VENTRAL_CORD_MOTORNEURONS
from cect.Cells import HSN_MOTORNEURONS
from cect.Cells import VC_HERM_MOTORNEURONS
from cect.Cells import INTERNEURONS_NONPHARYNGEAL_COOK
from cect.Cells import PHARYNGEAL_INTERNEURONS
from cect.Cells import PHARYNGEAL_MOTORNEURONS

from cect.Cells import get_standard_color

from cect.ConnectomeReader import DEFAULT_COLORMAP


class NodeSet:
    def __init__(self, name, cells, color=None, shape=None, position=None):
        self.name = name
        self.color = color
        self.cells = cells
        self.color = color
        self.shape = shape
        self.position = position

    def is_one_cell(self):
        return len(self.cells) == 1 and self.name == self.cells[0]

    def __repr__(self):
        return "NodeSet %s%s: %s" % (
            self.name,
            " (%s)"
            % (
                "%s%s" % (self.color, self.shape if self.shape is not None else "")
                if self.color is not None
                else ""
            ),
            self.cells,
        )


class View:
    def __init__(
        self,
        name,
        node_sets,
        synclass_sets={},
        colormap=DEFAULT_COLORMAP,
        only_show_existing_nodes=False,
    ):
        self.name = name
        self.node_sets = node_sets
        self.synclass_sets = synclass_sets
        self.colormap = colormap
        self.only_show_existing_nodes = only_show_existing_nodes

    def has_color(self):
        for ns in self.node_sets:
            if ns.color is not None:
                return True
        return False

    def get_node_set(self, node_set_name):
        for ns in self.node_sets:
            if ns.name == node_set_name:
                return ns
        return None

    def get_index_of_cell(self, cell):
        for i in range(len(self.node_sets)):
            if cell in self.node_sets[i].cells:
                return i
        return -1


EXC_INH_GJ_SYN_CLASSES = {
    "Chemical Exc": ["Acetylcholine", "Generic_CS"],
    "Chemical Inh": ["GABA"],
    "Electrical": ["Generic_GJ"],
}

CHEM_GJ_SYN_CLASSES = {
    "Chemical": EXC_INH_GJ_SYN_CLASSES["Chemical Exc"]
    + EXC_INH_GJ_SYN_CLASSES["Chemical Inh"],
    "Electrical": ["Generic_GJ"],
}

RAW_VIEW = View("Raw Data", [], CHEM_GJ_SYN_CLASSES, only_show_existing_nodes=True)
for cell in (
    sorted(PREFERRED_NEURON_NAMES)
    + sorted(PREFERRED_MUSCLE_NAMES)
    + sorted(KNOWN_OTHER_CELLS)
):
    RAW_VIEW.node_sets.append(NodeSet(cell, [cell], get_standard_color(cell)))


FULL_VIEW = View("Full View", [], EXC_INH_GJ_SYN_CLASSES)
for cell in (
    sorted(SENSORY_NEURONS_COOK)
    + sorted(INTERNEURONS_NONPHARYNGEAL_COOK)
    + sorted(
        HEAD_MOTORNEURONS_COOK
        + VENTRAL_CORD_MOTORNEURONS
        + SUBLATERAL_MOTORNEURONS_COOK
        + HSN_MOTORNEURONS
    )
    + sorted(PHARYNGEAL_NEURONS)
    + sorted(PHARYNGEAL_INTERNEURONS)
    + sorted(PHARYNGEAL_MOTORNEURONS)
):
    FULL_VIEW.node_sets.append(NodeSet(cell, [cell]))

PHARYNX_VIEW = View("Pharynx View", [], EXC_INH_GJ_SYN_CLASSES)
for cell in sorted(PHARYNGEAL_NEURONS):
    PHARYNX_VIEW.node_sets.append(NodeSet(cell, [cell]))

SOCIAL_VIEW = View("Social View", [], EXC_INH_GJ_SYN_CLASSES)
for cell in sorted(["RMGR", "ASHR", "ASKR", "AWBR", "IL2R", "RMHR", "URXR"]):
    SOCIAL_VIEW.node_sets.append(NodeSet(cell, [cell]))

SMALL_VIEW = View("Small View", [], CHEM_GJ_SYN_CLASSES)

sn_pos = {
    "SN1": (2, 2.8),
    "SN2": (6.1, 2.9),
    "SN3": (6, 4.3),
    "SN4": (2.4, 3.6),
    "SN5": (3.4, 5.3),
    "SN6": (4, 5.4),
}

for category in SENSORY_NEURONS_COOK_CATEGORIES:
    color = "#b31b1b"
    if category == "SN1":
        color = "#FFC0CB"
    SMALL_VIEW.node_sets.append(
        NodeSet(
            category,
            SENSORY_NEURONS_COOK_CATEGORIES[category],
            color=color,
            shape="triangle-up",
            position=sn_pos[category],
        )
    )

in_pos = {"IN1": (4.2, 3.3), "IN2": (3.4, 4.2), "IN3": (5.1, 4.4), "IN4": (2.3, 4.8)}

for category in INTERNEURONS_NONPHARYNGEAL_COOK_CATEGORIES:
    if category != "RIML":
        SMALL_VIEW.node_sets.append(
            NodeSet(
                category,
                INTERNEURONS_NONPHARYNGEAL_COOK_CATEGORIES[category],
                color="#16537E",
                shape="hexagon2",
                position=in_pos[category],
            )
        )

SMALL_VIEW.node_sets.append(
    NodeSet(
        "HMN",
        HEAD_MOTORNEURONS_COOK,
        color="#FFDF00",
        shape="circle",
        position=(3.2, 2.2),
    )
)

SMALL_VIEW.node_sets.append(
    NodeSet(
        "SMN",
        SUBLATERAL_MOTORNEURONS_COOK,
        color="#e59636",
        shape="circle",
        position=(4.5, 2.2),
    )
)

SMALL_VIEW.node_sets.append(
    NodeSet(
        "MNVC",
        VENTRAL_CORD_MOTORNEURONS,
        color="#B2832b",
        shape="circle",
        position=(7.1, 1),
    )
)

SMALL_VIEW.node_sets.append(
    NodeSet(
        "VC", VC_HERM_MOTORNEURONS, color="#FF00FF", shape="circle", position=(7.8, 3.3)
    )
)

SMALL_VIEW.node_sets.append(
    NodeSet(
        "HSN", HSN_MOTORNEURONS, color="#FF00FF", shape="circle", position=(6.3, 5.9)
    )
)

SMALL_VIEW.node_sets.append(
    NodeSet(
        "MUBODY", BODY_MUSCLES_COOK, color="#5a2d0d", shape="square", position=(5, 0.73)
    )
)
SMALL_VIEW.node_sets.append(
    NodeSet(
        "MUHEAD", HEAD_MUSCLES_COOK, color="#5a2d0d", shape="square", position=(3.1, 1)
    )
)


ALL_VIEWS = [RAW_VIEW, FULL_VIEW, PHARYNX_VIEW, SOCIAL_VIEW, SMALL_VIEW]


if __name__ == "__main__":
    ns_v = NodeSet("Vmn", ["VA6", "VB6", "VB3", "VD6", "VA3", "VD3", "VB2"])
    ns_d = NodeSet("Dmn", ["DB4", "DD4"])
    ns_p = NodeSet("PVCL", ["PVCL"])
    ns_a = NodeSet("AVBL", ["AVBL"])

    v1 = View("VandD", [ns_d, ns_v, ns_a, ns_p], EXC_INH_GJ_SYN_CLASSES)

    from cect.TestDataReader import tdr_instance

    print(NodeSet(SMALL_VIEW, SMALL_VIEW))

    print(tdr_instance.summary())

    print("----------------")
    print(tdr_instance.get_connectome_view(v1).summary())

    print("----------------")
    print(tdr_instance.get_connectome_view(SOCIAL_VIEW).summary())
