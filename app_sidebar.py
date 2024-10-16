import streamlit as st
from src.visualization_functions import visualize_test_results
from src.result_display_functions import two_by_two

st.set_page_config(
    page_title="Medical Test Simulation",
    page_icon=":pill:",
    layout="wide",  # Use the "wide" layout
    initial_sidebar_state="expanded",  # Keep the sidebar expanded
)


def app():
    st.title("Medical Test Simulation")

    # Sidebar for input
    with st.sidebar:
        st.header("Input")
        population_size = st.number_input(
            "Population Size",
            min_value=1000,
            max_value=1000000000,
            value=1000,
            step=1000,
        )
        disease_name = st.text_input("Disease Name", value="Disease A")
        prevalence = st.number_input(
            "Prevalence",
            min_value=0.000001,
            max_value=1.0,
            value=0.05,
            step=0.001,
            format="%.5f",
        )

        sensitivity = st.slider("Sensitivity", 0.0, 1.0, 0.9, 0.01)
        specificity = st.slider("Specificity", 0.0, 1.0, 0.7, 0.01)

        # Create population data dictionary
        population_data = {
            "size": population_size,
            "conditions": {disease_name: prevalence},
        }

    # Main page for results
    (
        col1,
        col2,
    ) = st.columns(2)

    # Run simulation and visualization
    if st.sidebar.button("Run Simulation"):
        fig1, fig2, messages, test_results = visualize_test_results(
            population_data,
            disease_name,
            sensitivity,
            specificity,
            grid_size=20,
        )
        with col1:
            if fig1 and fig2:
                st.pyplot(fig1)
                st.pyplot(fig2)
                st.write(messages)
            else:
                st.error(messages)
        with col2:
            table = two_by_two(test_results)
            st.dataframe(table)
            st.write(test_results)


if __name__ == "__main__":
    app()
