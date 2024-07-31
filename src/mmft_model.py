from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Union
from enum import Enum
from pydantic.alias_generators import to_camel

config = ConfigDict(
    strict=True, extra="forbid", validate_assignment=True, alias_generator=to_camel
)


class Info(BaseModel):
    model_config = config

    id: str
    name: str
    cat: Optional[str] = Field(
        default=None,
        description="Margin refers to the safety margin setting of the designer",
    )
    margin: float


class Geometry(BaseModel):
    model_config = config

    width: float = Field(gt=0, description="Width of the chip in meters")
    height: float = Field(gt=0, description="Height of the chip in meters")
    depth: float = Field(gt=0, description="Depth of the chip in meters")


class NodeMesh(BaseModel):
    model_config = config

    """TBD; will contain 3d vertices and normals"""


class Node(BaseModel):
    model_config = config

    x: float
    y: float
    z: Optional[float] = Field(default=0)
    diameter: Optional[float] = None
    mesh: Optional[NodeMesh] = None
    f_3dexport: Optional[bool] = Field(
        alias="3dexport",
        default=False,
        description="If set, the node has a 3d representation",
    )
    virtual: Optional[bool] = None
    hsa: Optional[bool] = Field(default=None, alias="HSA")
    ground: Optional[bool] = None


class ChannelMesh(BaseModel):
    model_config = config

    """TBD; will contain 3d vertices and normals"""


class ChannelGenerator(BaseModel):
    model_config = config

    """TBD; may include Meander parameters, etc.."""


class Channel(BaseModel):
    model_config = config

    node1: int
    node2: int
    width: float
    height: float
    mesh: Optional[ChannelMesh] = None
    generator: Optional[ChannelGenerator] = None
    bypass: Optional[bool] = None
    hsa: Optional[bool] = Field(default=None, alias="HSA")
    virtual: Optional[bool] = None


class Module(BaseModel):
    model_config = config

    position: tuple[float, float, float]
    size: tuple[float, float, float]
    nodes: list[int]


class Label(BaseModel):
    model_config = config

    text: str = Field(
        description="User-defined labels to document chip / experiment design considerations"
    )
    x: float
    y: float


class Network(BaseModel):
    model_config = config

    info: Info
    geometry: Geometry
    nodes: list[Node]
    channels: list[Channel]
    modules: list[Module]
    labels: list[Label]


class Platform(str, Enum):
    CONTINUOUS = "continuous"
    BIGDROPLET = "bigdroplet"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


class Type(str, Enum):
    ABSTRACT = "abstract"
    HYBRID = "hybrid"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


class ResistanceModel(str, Enum):
    RESTANGULAR = "rectangular"
    POISEUILLE = "poiseuille"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


class MixingModel(str, Enum):
    INSTANTANEOUS = "instantaneous"
    DIFFUSIVE = "diffusive"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


class Color(BaseModel):
    model_config = config

    r: int = Field(ge=0, lt=256, alias="R")
    g: int = Field(ge=0, lt=256, alias="G")
    b: int = Field(ge=0, lt=256, alias="B")
    a: int = Field(ge=0, lt=256, alias="A")


class Fluid(BaseModel):
    model_config = config

    id: str
    name: str
    color: Color
    concentration: float = Field(ge=0, le=1)
    density: float
    viscosity: float


class Species(BaseModel):
    model_config = config

    id: str
    name: str
    color: Color
    diffusivity: float = Field(
        description="Diffusivity is the value for the species in the continuous phase in m^2/s"
    )
    saturation_concentration: float = Field(
        description="Saturation concentration is in g/m^3"
    )


class Mixture(BaseModel):
    model_config = config

    species: list[int]
    concentrations: list[float] = Field(
        description="Concentration can never be higher than the respective saturation concentration"
    )


class PumpType(str, Enum):
    FLOWRATEPUMP = "flowratepump"
    PRESSUREPUMP = "pressurepump"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None


class Pump(BaseModel):
    model_config = config

    channel: int
    name: str
    color: Color
    type: PumpType


class BoundaryCondition(BaseModel):
    model_config = config

    pump: int
    delta_p: Optional[float] = None
    flow_rate: Optional[float] = None


class BigDropletInjection(BaseModel):
    model_config = config

    fluid: int
    volume: float
    channel: int
    pos: float
    delta_t: Optional[float] = Field(ge=0, default=None, description="If given and > 0, injections occur in regular intervals until the simulation ends, or t1")
    t0: float
    t1: float


class MixtureInjection(BaseModel):
    model_config = config

    mixture: int
    channel: int
    t0: float


class Fixture(BaseModel):
    model_config = config

    name: str
    phase: int
    boundary_conditions: list[BoundaryCondition]
    big_droplet_injections: list[BigDropletInjection]
    mixture_injections: list[MixtureInjection]

class SimulatorType(str, Enum):
    LMB = "lbm"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None
    
class OpeningNormal(BaseModel):
    model_config = config

    x: float
    y: float
    z: float

class Opening(BaseModel):
    model_config = config

    node: int
    normal: OpeningNormal = Field(description="This should be a unit vector, but the conversion can better be done in the back-end. For now 'z' is probably always zero, if we don't consider fully 3D network structures.")

class RectangularChannelOpening(Opening):
    model_config = config

    width: Optional[float] = None
    height: Optional[float] = None

class CylindricalChannelOpening(Opening):
    model_config = config

    radius: Optional[float] = Field(default=None, description="Circular opening for when a cylindrical channel connects to the module")


class Simulator(BaseModel):
    model_config = config

    type: SimulatorType
    name: str
    stl_content: Optional[str] = None
    stl_file: Optional[str] = None
    char_phys_length: float
    char_phys_velocity: float
    alpha: float
    resolution: float
    epsilon: float
    tau: float
    module_id: int
    openings: list[Union[RectangularChannelOpening, CylindricalChannelOpening]]

class SimulationSettings(BaseModel):
    model_config = config

    duration: float = Field(description="In seconds.")
    position: float
    step: float = Field(description="In seconds.")
    loop: bool
    vtk_folder: str
    simulators: list[Simulator]


class Simulation(BaseModel):
    model_config = config

    platform: Platform
    type: Type
    resistance_model: ResistanceModel
    mixing_model: MixingModel
    fluids: list[Fluid]
    species: list[Species]
    mixtures: list[Mixture]
    pumps: list[Pump]
    fixtures: list[Fixture]
    activeFixture: int
    settings: SimulationSettings


class ResultType(str, Enum):
    _1D = "1d"

    @classmethod
    def _missing_(cls, value):
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None

class Result(BaseModel):
    model_config = config

    fixture: int
    type: ResultType

class BasicResult(Result):
    model_config = config

    data: str = Field(description="For now, 1D simulator results are stored 1:1 in the data field; later, they should be adapted to fit in the hybrid sim scheme")


class ExtensiveResult(Result):
    model_config = config

    platform: Platform
    #fluids: list[ResultFluid]


class Settings(BaseModel):
    model_config = config

    align_node_to_grid: bool
    default_channel_height: float
    default_channel_width: float
    default_date_time_fmt: str
    default_droplet_volume: float
    default_node_diameter: float
    default_simulation_duration: int
    grid_color_argb: int = Field(alias='gridColorARGB') # Temporary fix, this is not canonic
    grid_distance: float
    hybrid_sim_server_address: str
    hybrid_sim_server_port: int
    log_date_time: bool
    log_severity: bool
    show_designer_info: bool
    show_designer_sim_info: bool
    show_grid: bool
    show_nodes: bool
    show_chip_area: bool
    simulation_speed: float
    svg_export_dimensions: float


class MMFTDataModel(BaseModel):
    model_config = config

    network: Network
    simulation: Optional[Simulation] = None
    results: Optional[list[Union[BasicResult, ExtensiveResult]]] = None
    settings: Optional[Settings] = None
    log: Optional[str] = Field(default=None, description="contains the entire designer log output at the time of export")
