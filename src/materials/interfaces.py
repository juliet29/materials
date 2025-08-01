from enum import StrEnum
from typing import TypedDict

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




class NRMCAEntry(TypedDict):
    imperial_psi: tuple[int, int]
    gwp: list[int]

# class CompanyEntry(TypedDict):
#     company: str
#     imperial_psi: tuple[int, int]
#     alteration_details: str
#     gwp: int
#     gwp_unit: str



class Entry(TypedDict):
    company: str
    imperial_psi: tuple[int, int]
    gwp: float
    gwp_unit: str
    alteration_details: str
    alteration_details_print_name: str


