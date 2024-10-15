import matplotlib.pyplot as plt
from pywaffle import Waffle
from src.simulation_functions import (
    generate_testing_population,
    perform_test,
    calculate_test_metrics
)
import streamlit as st

def make_waffle(results_dict: dict):
    fig1 = plt.figure(
        FigureClass=Waffle,
        rows=5,
        columns=10,
        values={
            k: v
            for k, v in results_dict.items()
            if k in ["true_positives", "false_positives"]
        },
        icon_size=20,
        legend={"loc": "upper left", "bbox_to_anchor": (1.05, 1)},
        colors=[  "#56ae6c", "#fe6e6c",],
        title={"label": "People who got a positive test", "loc": "center"},
        icons=['face-meh', 'face-frown'],
        vertical=False,
        block_arranging_style="new-line",
        starting_location="NW",
    )

    fig2 = plt.figure(
        FigureClass=Waffle,
        rows=5,

        columns=10,
        values={
            k: v
            for k, v in results_dict.items()
            if k in ["true_negatives", "false_negatives"]
        },
        icon_size=20,
        legend={"loc": "upper left", "bbox_to_anchor": (1.05, 1)},
        colors=["#719a78", "#fe6e6c"],
        title={"label": "People who got a negative test", "loc": "center"},
        icons=['face-smile', 'face-frown'],
        vertical=False,
        block_arranging_style="new-line",
        starting_location="NW",
    )

    return fig1, fig2


def visualize_test_results(pop_dict, condition, sensitivity, specificity, grid_size):
    """
    Visualizes the results of a diagnostic test simulation.

    Args:
        pop_dict: A dictionary containing population parameters.
        condition: The name of the condition column.
        sensitivity: The sensitivity of the test.
        specificity: The specificity of the test.
        grid_size: The size of the grid for the waffle chart visualization.
    """
    messages = ""
    try:
        df, gen_message = generate_testing_population(pop_dict)
        messages += gen_message
        if df is not None:
            t_df, test_message = perform_test(df, condition, sensitivity, specificity)
            messages += test_message
            if t_df is not None:
                results, metrics_message = calculate_test_metrics(t_df, condition)  
                messages += metrics_message
                fig1, fig2 = make_waffle(results)
                st.write("**Test Metrics:**")
                for metric, value in results.items():
                    st.write(f"{metric}: {value}")

                return fig1, fig2, messages
            else:
                messages += "Error: Good news, no one has this condition! \nBad news, we need sick people!"
                return None, None, messages
        else:
            messages += "Error: Failed to generate testing population."
            return None, None, messages

    except Exception as e:
        messages += f"An error occurred: {e}"
        return None, None, messages
