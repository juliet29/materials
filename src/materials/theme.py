import altair as alt
import materials.colors as colors

CLEARVIEW = "ClearviewText"
FONT = f'{CLEARVIEW}, system-ui, -apple-system, BlinkMacSystemFont, ".SFNSText-Regular", sans-serif'
FONT_SIZE = 14
LABEL_FONT_SIZE = 12
FONT_COLOR = "#161616"
LABEL_COLOR = "#525252"
DEFAULT_WIDTH = 350


@alt.theme.register("scape", enable=True)
def scape() -> alt.theme.ThemeConfig:
    return {
        "config": {
            "view": {
                "width": 350,
                "height": 280,
            },
            "axis": {
                "labelColor": LABEL_COLOR,
                "labelFontSize": LABEL_FONT_SIZE,
                "labelFont": FONT,
                "labelFontWeight": 400,
                "titleColor": FONT_COLOR,
                "titleFontWeight": 400,
                "titleFontSize": FONT_SIZE,
                "titleFont": FONT,
            },
            "axisX": {"titlePadding": 10},
            "axisY": {"titlePadding": 2.5},
            "text": {"font": FONT, "fontSize": FONT_SIZE},
            "range": {
                "ordinal": colors.single_hue,  # TODO should be single hue
                "category": list(reversed(colors.categorical_teal_orange)),
                "sequential": colors.single_hue,
                "diverging": colors.diverging_teal_red,
            },  # type: ignore
            "legend": {
                "labelFont": FONT,
                "labelFontSize": LABEL_FONT_SIZE,
                "labelLimit": 500,
            },
        }
    }
