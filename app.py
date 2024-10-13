import streamlit as st
from src.visualization_functions import visualize_test_results


st.set_page_config(
    page_title="Medical Test Simulation",
    page_icon=":pill:",
    layout="wide",  # Use the "wide" layout
    initial_sidebar_state="collapsed",  # Collapse the sidebar
)


def app():
    st.title("Medical Test Simulation")

    (
        col1,
        col2,
    ) = st.columns(2)
    # Get form inputs
    with col1:
        st.header("Input")
        population_size = st.number_input(
            "Population Size", min_value=1, value=1000, step=1
        )
        conditions = st.text_input(
            "Conditions (comma-separated)", value="Condition A, Condition B"
        )
        prevalences = st.text_input("Prevalences (comma-separated)", value="0.1, 0.2")
        test_condition = st.selectbox("Test Condition", conditions.split(","))
        sensitivity = st.slider("Sensitivity", 0.0, 1.0, 0.8, 0.01)
        specificity = st.slider("Specificity", 0.0, 1.0, 0.9, 0.01)

        # Create population data dictionary
        conditions = [c.strip() for c in conditions.split(",")]
        prevalences = [float(p) for p in prevalences.split(",")]
        population_data = {
            "size": population_size,
            "conditions": {c: p for c, p in zip(conditions, prevalences)},
        }

    # Run simulation and visualization
    if st.button("Run Simulation"):
        fig1, fig2, messages = visualize_test_results(
            population_data, test_condition, sensitivity, specificity, grid_size=20
        )
        with col2:
            st.header("Results")
            if fig1 and fig2:
                st.pyplot(fig1)
                st.pyplot(fig2)
                st.write(messages)
            else:
                st.error(messages)


if __name__ == "__main__":
    app()
