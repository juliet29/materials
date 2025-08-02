import altair as alt
import polars as pl

from materials.dataframes import combine_data
import materials.columns as col
from materials.interfaces import ConcreteAlteration

# TODO make this a method..


# def prep_df(df: pl.DataFrame):
#     df.with_columns(pl.when())
#     # filter unknowns
#     # get the values of gwp at the max psi w/in the cayegory groups
#     # sort from greatest to least psi
#     # assign a diff if two things are similar


def scatter_plot(df: pl.DataFrame):
    base_chart = alt.Chart(df).encode(
        x=alt.X(col.IMPERIAL_PSI_MAX).scale(zero=False),
        y=alt.Y(col.GWP).scale(zero=False),
    )

    base_industry_chart = base_chart.transform_filter(
        alt.datum[col.ALTERATION_DETAILS_PRINT_NAME]
        != ConcreteAlteration._100_UNKNOWN.value
    )

    industry = base_industry_chart.mark_line(point=True).encode(
        color=alt.Color(col.ALTERATION_DETAILS_PRINT_NAME).legend(
            orient="bottom",
        ),
    )

    last_strength = (
        base_industry_chart.mark_circle(size=100)
        .encode(
            alt.X(f"last_strength[{col.IMPERIAL_PSI_MAX}]:Q"),
            alt.Y(f"last_strength[{col.GWP}]:Q"),
            color=alt.Color(col.ALTERATION_DETAILS_PRINT_NAME),
        )
        .transform_aggregate(
            last_strength=f"argmax({col.IMPERIAL_PSI_MAX})",
            groupby=[col.ALTERATION_DETAILS_PRINT_NAME],
        )
    )
    label_calc = (
        last_strength.transform_window(
            sort=[{"field": f"last_strength[{col.GWP}]"}],
            frame=[0, 0],
            min_group=f"lag(last_strength[{col.GWP}])",
            max_group=f"first_value(last_strength[{col.GWP}])",
            values=f"values(last_strength[{col.GWP}])",
        )
        .transform_calculate(difference=alt.datum.max_group - alt.datum.min_group)
        .transform_calculate(
            custom_dx=alt.expr.if_(alt.datum.difference < 10, 10, 10),
            custom_dy=alt.expr.if_(alt.datum.difference < 10, 12, 0),
        )
    )

    alteration_name = label_calc.mark_text(
        align="left",
        dx=alt.expr(alt.datum.custom_dx),  # type: ignore
        dy=alt.expr(alt.datum.custom_dy),  # type: ignore
    ).encode(
        text=alt.Text(
            col.ALTERATION_DETAILS_PRINT_NAME,
        ),  # col.ALTERATION_DETAILS_PRINT_NAME
    )
    # alteration_name2 = label_calc.mark_text(align="left", dx=50).encode(
    #     text="max_group:N"  # col.ALTERATION_DETAILS_PRINT_NAME
    # )
    # alteration_name3 = label_calc.mark_text(align="left", dx=120).encode(
    #     text="difference:N"  # col.ALTERATION_DETAILS_PRINT_NAME
    # )

    chart = (
        industry
        + last_strength
        + alteration_name  # + alteration_name2 + alteration_name3
    )  # + companies

    chart.show()


if __name__ == "__main__":
    alt.renderers.enable("browser")
    df = combine_data()
    scatter_plot(df)
