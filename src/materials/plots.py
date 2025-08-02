import altair as alt
import polars as pl

from materials import colors
from materials.dataframes import combine_data
import materials.columns as col
from materials.interfaces import ConcreteAlteration
from materials.theme import scape as scape


X_AXIS_CONCRETE_STRENGTH = "Concrete Strength [PSI]"
Y_AXIS_GWP = "Embodied Carbon Emissions [kg-co2-eq/m3]"


def scatter_plot(df: pl.DataFrame):
    alt.theme.enable("scape")
    base_chart = alt.Chart(df).encode(
        x=alt.X(f"{col.IMPERIAL_PSI_MAX}:Q")
        .scale(zero=False)
        .title(X_AXIS_CONCRETE_STRENGTH),
        y=alt.Y(f"{col.GWP}:Q").scale(zero=False).title(Y_AXIS_GWP),
    )

    base_industry_chart = base_chart.transform_filter(
        alt.datum[col.ALTERATION_DETAILS_PRINT_NAME]
        != ConcreteAlteration._100_UNKNOWN.value
    )

    industry = base_industry_chart.mark_line(point=True).encode(
        color=alt.Color(f"{col.ALTERATION_DETAILS_PRINT_NAME}:O").legend(None),
    )

    last_strength = (
        base_industry_chart.mark_circle(size=100)
        .encode(
            alt.X(f"last_strength[{col.IMPERIAL_PSI_MAX}]:Q"),
            alt.Y(f"last_strength[{col.GWP}]:Q"),
            color=alt.Color(f"{col.ALTERATION_DETAILS_PRINT_NAME}:O").legend(
                orient="bottom", columns=2
            ),
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
        )  # TODO, could try to calculate the width of text.. / num characters
        .transform_calculate(difference=alt.datum.max_group - alt.datum.min_group)
        .transform_calculate(
            custom_dy=alt.expr.if_(alt.datum.difference < 10, 15, 0),
        )
    )

    alteration_name = label_calc.mark_text(
        align="left",
        dx=10,  # type: ignore
        dy=alt.expr(alt.datum.custom_dy),  # type: ignore
    ).encode(
        text=alt.Text(
            col.ALTERATION_DETAILS_PRINT_NAME,
        ),
    )

    companies = (
        base_chart.mark_point(
            size=400, opacity=1, filled=True, color=colors.categorical_teal_orange[-1]
        )
        .encode(
            shape=alt.Shape(f"{col.COMPANY}:N").legend(orient="bottom"),
        )
        .transform_filter(
            alt.datum[col.ALTERATION_DETAILS] == ConcreteAlteration._100_UNKNOWN.name
        )
    )

    chart = (
        industry
        + last_strength
        + alteration_name
        + companies  # + alteration_name2 + alteration_name3
    ).properties(height=500)  # + companies

    chart.show()


if __name__ == "__main__":
    alt.renderers.enable("browser")
    df = combine_data()
    scatter_plot(df)
