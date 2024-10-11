from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
from src.visualization_functions import visualize_test_results_con

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get form data
            population_size = int(request.form["population_size"])
            conditions = request.form["conditions"].split(",")
            prevalences = [float(p) for p in request.form["prevalences"].split(",")]
            test_condition = request.form["test_condition"]
            sensitivity = float(request.form["sensitivity"])
            specificity = float(request.form["specificity"])

            # Create population data dictionary
            population_data = {
                "size": population_size,
                "conditions": {c.strip(): p for c, p in zip(conditions, prevalences)},
            }

            # Run simulation and visualization
            plot_data1, plot_data2, messages = visualize_test_results_con(
                population_data,
                test_condition,
                sensitivity,
                specificity,
                grid_size=20
            )

            if plot_data1 and plot_data2:
                return render_template(
                    "result.html",
                    plot_data1=plot_data1,
                    plot_data2=plot_data2,
                    messages=messages
                )
            else:
                return render_template("error.html", error_message=messages)
        except Exception as e:
            return render_template("error.html", error_message=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)