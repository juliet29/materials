from typing import TypedDict
from materials.paths import static_paths, PATH_TO_COMPANIES_DATA, PATH_TO_NRMCA_DATA
from utils4plans.io import read_json
from utils4plans.lists import chain_flatten
import polars as pl
from enum import StrEnum
from rich import print as rprint

# TODO these are data-derived constants that should be moved and documented
NRMCA_UNIT = "kg-co2e_m3"
NRMCA_COMPANY = "NRMCA"
GWP_FOR_CURRENT_ALTERATION_CONCERN = slice(0, 8)


class ConcreteAlteration(StrEnum):
    # min amount
    # TODO fix strings
    _0_FLY_ASH_SLAG_0 = r"0-19% Fly Ash and/or Slag"
    _1_FLY_ASH_20 = r"20-29% Fly Ash"
    _2_FLY_ASH_30 = r"30-39% Fly Ash"
    _3_FLY_ASH_40 = r"40-49% Fly Ash"
    _4_SLAG_30 = r"30-39% Slag"
    _5_SLAG_40 = r"40-49% Slag"
    _6_SLAG_50 = r">50% Slag"
    _7_FLY_ASH_20_SLAG_30 = r">20% Fly Ash and >30%Slag"
    _100_UNKNOWN = "Unknown"


class Entry(TypedDict):
    company: str
    imperial_psi_min: int
    imperial_psi_max: int
    alteration_details: str
    alteration_details_print_name: str
    gwp: int
    gwp_unit: str


class CompanyEntry(TypedDict):
    company: str
    imperial_psi: tuple[int, int]
    alteration_details: str
    gwp: int
    gwp_unit: str


class NRMCAEntry(TypedDict):
    imperial_psi: tuple[int, int]
    gwp: list[int]


def get_data():
    companies_data = read_json(static_paths.inputs, PATH_TO_COMPANIES_DATA)
    return companies_data


def process_nrmca_data():
    def expand_entry(entry: NRMCAEntry):
        alter_at_gwp = {
            alter: num
            for alter, num in zip(
                ConcreteAlteration, entry["gwp"][GWP_FOR_CURRENT_ALTERATION_CONCERN]
            )
        }

        new_entries = []
        for alteration, gwp in alter_at_gwp.items():
            new_entry: Entry = {
                "company": NRMCA_COMPANY,
                "imperial_psi_min": entry["imperial_psi"][0],
                "imperial_psi_max": entry["imperial_psi"][1],
                "alteration_details": alteration.name,
                "alteration_details_print_name": alteration.value,
                "gwp": gwp,
                "gwp_unit": NRMCA_UNIT,
            }
            new_entries.append(new_entry)
        return new_entries

    nrmca_data: list[NRMCAEntry] = read_json(static_paths.inputs, PATH_TO_NRMCA_DATA)
    result = chain_flatten([expand_entry(i) for i in nrmca_data])
    return pl.from_dicts(result)
    # test expand psi


if __name__ == "__main__":
    process_nrmca_data()
