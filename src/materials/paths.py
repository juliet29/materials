import pyprojroot
from pathlib import Path
from dataclasses import dataclass
from utils4plans.io import check_folder_exists_and_return
from enum import StrEnum

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
STATIC = "static"


class FolderStructure(StrEnum):
    INPUTS = "_01_inputs"  # input data 
    TEMP = "_04_temp"  # pickled files
    FIGURES = "_05_figures"


@dataclass(frozen=True)
class StaticPaths:
    # name: str
    base_path: Path

    def get_data_folder(self, folder: FolderStructure):
        return check_folder_exists_and_return(self.base_path / STATIC / folder)

    @property
    def inputs(self):
        return self.get_data_folder(FolderStructure.INPUTS)

    @property
    def figures(self):
        return self.get_data_folder(FolderStructure.FIGURES)

    @property
    def temp(self):
        return self.get_data_folder(FolderStructure.TEMP)


static_paths = StaticPaths(
    BASE_PATH
)  # TODO: not sure should have to instantiate this... feel like BASE_PATH should be default..
# _01_inputs
PATH_TO_COMPANIES_DATA = Path("companies/companies")
PATH_TO_NRMCA_DATA = Path("nrmca_2023/nrmca_2023")
