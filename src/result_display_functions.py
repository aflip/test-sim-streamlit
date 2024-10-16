# functions for pretty display of the test results
import polars as pl
from great_tables import loc, style
import pandas as pd
import numpy as np


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

    # df.style.tab_style(
    #     style.text(font="Georgia"),
    #     loc.body(columns="Actual Negative"),
    # )

    return df

# Turned off the styling because styling doesnt work in streamlit. 
# def two_by_two_pd(results_dict):
#     df = pd.DataFrame(
#         {
#             "": ["Tested Positive", "Tested Negative"],
#             "Actual Positive": [
#                 results_dict["true_positives"],
#                 results_dict["false_negatives"],
#             ],
#             "Actual Negative": [
#                 results_dict["false_positives"],
#                 results_dict["true_negatives"],
#             ],
#         }
#     )
#     props = 'font-family: "Times New Roman", Times, serif; color: #e83e8c; font-size:1.3em;'
#     df.style.set_table_styles([{'selector': 'td.col1', 'props': props}])

#     return df

#     # return styled_df
