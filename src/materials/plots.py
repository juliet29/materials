import altair as alt
import polars as pl

from materials.dataframes import combine_data
import materials.columns as col
from materials.interfaces import ConcreteAlteration

# TODO make this a method..


def scatter_plot(df: pl.DataFrame):
    base_chart = alt.Chart(df).encode(
        x=alt.X(col.IMPERIAL_PSI_MAX).scale(zero=False),
        y=alt.Y(col.GWP).scale(zero=False),
    )
    industry = (
        base_chart.mark_line(point=True).encode(
            color=alt.Color(col.ALTERATION_DETAILS_PRINT_NAME).sort(
                [i.value for i in ConcreteAlteration]
            ),
        )
    ).transform_filter(
        alt.datum[col.ALTERATION_DETAILS] != ConcreteAlteration._100_UNKNOWN.name
    )

    companies = (
        base_chart.mark_circle(size=400, opacity=1)
        .encode(color=alt.Color(col.COMPANY))
        .transform_filter(
            alt.datum[col.ALTERATION_DETAILS] == ConcreteAlteration._100_UNKNOWN.name
        )
    )

    chart = industry + companies

    chart.show()


if __name__ == "__main__":
    alt.renderers.enable("browser")
    df = combine_data()
    scatter_plot(df)
