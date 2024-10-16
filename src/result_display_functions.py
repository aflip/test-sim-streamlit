# functions for pretty display of the test results
import polars as pl
import streamlit as st

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
    return df

