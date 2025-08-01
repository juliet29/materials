from materials.interfaces import (
    HEIDELBERG_MIN_SAVINGS,
    CompanyNames,
    ConcreteAlteration,
    Entry,
    NRMCAEntry,
)
from materials.paths import static_paths, PATH_TO_COMPANIES_DATA, PATH_TO_NRMCA_DATA
from utils4plans.io import read_json
from utils4plans.lists import chain_flatten
import polars as pl
from rich import print as rprint
from copy import deepcopy
import materials.columns as col

# TODO these are data-derived constants that should be moved and documented
NRMCA_UNIT = "kg-co2e_m3"
NRMCA_COMPANY = "NRMCA"
GWP_FOR_CURRENT_ALTERATION_CONCERN = slice(0, 8)


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
                "imperial_psi": entry["imperial_psi"],
                "gwp": gwp,
                "gwp_unit": NRMCA_UNIT,
                "alteration_details": alteration.name,
                "alteration_details_print_name": alteration.value,
            }
            new_entries.append(new_entry)
        return new_entries

    nrmca_data: list[NRMCAEntry] = read_json(static_paths.inputs, PATH_TO_NRMCA_DATA)
    result = chain_flatten([expand_entry(i) for i in nrmca_data])
    return pl.from_dicts(result)
    # test expand psi


def process_companies_data():
    companies_data: list[Entry] = read_json(static_paths.inputs, PATH_TO_COMPANIES_DATA)
    for entry in companies_data:
        entry["alteration_details"] = ConcreteAlteration._100_UNKNOWN.name
        entry["alteration_details_print_name"] = ConcreteAlteration._100_UNKNOWN.value

    df = pl.from_dicts(companies_data)  # pyright: ignore[reportArgumentType]
    rprint(df)

    return df


def edit_heidelberg_data(df: pl.DataFrame) -> pl.DataFrame:
    def calc_remain_perc_after_savings(savings: float):
        return 1 - savings
    # TODO better -> duplicate rows.. 
    return df.with_columns(
        pl.when(pl.col(col.COMPANY) == CompanyNames.HEIDELBERG.value)
        .then(pl.col(col.GWP) * calc_remain_perc_after_savings(HEIDELBERG_MIN_SAVINGS))
        .otherwise(pl.col(col.GWP))
        .alias(col.GWP)
    )


def combine_data():
    companies = process_companies_data()
    # rprint(companies)
    nrmca = process_nrmca_data()
    # rprint(nrmca)

    df = (
        pl.concat([nrmca, companies], how="vertical_relaxed")
        .select(
            [
                pl.all().exclude([col.IMPERIAL_PSI]),
                pl.col(col.IMPERIAL_PSI).list.get(0).alias(col.IMPERIAL_PSI_MIN),
                pl.col(col.IMPERIAL_PSI).list.get(1).alias(col.IMPERIAL_PSI_MAX),
            ]
        )
        .pipe(edit_heidelberg_data)
    )
    # rprint(df)
    return df


if __name__ == "__main__":
    combine_data()
