# functions for pretty display of the test results
import polars as pl
from great_tables import loc, style


def two_by_two(results):
    """Display two by two table of test results.
    Arguments: results: a dictionary
    """

    df = pl.DataFrame(
        {
            "": ["Tested Positive", "Tested Negative"],
            "Actual Positive": [results["true_positives"], results["false_negatives"]],
            "Actual Negative": [results["false_positives"], results["true_negatives"]],
        }
    )

    df.style.tab_style(
        style.text(font="Georgia"),
        loc.body(columns="Actual Negative"),
    )

    return df
