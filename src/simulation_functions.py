import polars as pl
import numpy as np
import math


def generate_testing_population(population_data_dict) -> (pl.DataFrame, str):
    """
    Generates a testing population DataFrame with conditions based on prevalence.

    Args:
        population_data_dict: A dictionary containing 'size' (int) for population size and
                         'conditions' (dict) where keys are condition names and values
                         are their prevalence rates (between 0 and 1).

    Returns:
        A tuple containing a polars DataFrame with condition columns, where each row represents a person,
        and a string with messages to be displayed.
    """
    messages = ""

    if (
        population_data_dict["size"] <= 30
        or len(population_data_dict["conditions"]) == 0
    ):
        messages += "Error: No one home! Population is not large enough!\n"
        return None, messages

    low_prevalence_conditions = [
        condition
        for condition, value in population_data_dict["conditions"].items()
        if value <= 1 / population_data_dict["size"]
    ]
    if low_prevalence_conditions:
        messages += f"Error: Good news: Not enough patients! \nBad news: Population is not large enough to support the given prevalence for: {', '.join(low_prevalence_conditions)}\n"
        return None, messages

    else:
        population_size = population_data_dict["size"]
        conditions_prevalence = population_data_dict["conditions"]

    data = {}
    for condition, prevalence in conditions_prevalence.items():
        data[condition] = np.random.choice(
            [True, False], size=population_size, p=[prevalence, 1 - prevalence]
        )
    # messages are being repeated, am unifying them
    # messages += "\nPrevalence of conditions in the generated population:\n"
    # for condition in list(population_data_dict["conditions"].keys()):
    #     messages += f"{condition}: {data[condition].mean():.2%}\n"
    # messages += "\n-------------------------------------------\n"
    return pl.DataFrame(data), messages


def perform_test(
    data: pl.DataFrame,
    condition: str,
    t_sensitivity: float,
    t_specificity: float,
) -> (pl.DataFrame, str):
    """
    Simulates a test with given sensitivity and specificity on a Polars DataFrame.

    Args:
        data: A Polars DataFrame with conditions as columns
        condition: The condition to test for
        sensitivity: The sensitivity of the test (true positive rate)
        specificity: The specificity of the test (true negative rate)

    Returns:
        A tuple containing a Polars DataFrame with true conditions and simulated test results,
        and a string with messages to be displayed.
    """
    messages = ""

    if condition not in data.columns:
        messages += f"{condition} not found in the population!, try with one of these conditions {data.columns}\n"
        return None, messages
    true_conditions = data[condition].to_numpy()
    size = data.height

    # Check if there is at least one true condition
    if np.any(true_conditions):
        # Simulate test outcomes based on sensitivity and specificity
        test_results = np.where(
            true_conditions,
            np.random.rand(size) < t_sensitivity,  # True positives and false negatives
            np.random.rand(size) >= t_specificity,  # False positives and true negatives
        )
    else:
        messages += "Error:Population too fit! No one here has this problem, try again with a different condition\n"
        return messages
    result_df = pl.DataFrame(
        {
            "true_condition": true_conditions,
            "test_result": test_results,
        }
    )

    return result_df, messages


def calculate_test_metrics(t_df: pl.DataFrame, condition: str) -> (dict, str):
    messages = ""
    tp = t_df.filter((pl.col("true_condition")) & (pl.col("test_result"))).height
    tn = t_df.filter((~pl.col("true_condition")) & (~pl.col("test_result"))).height
    fp = t_df.filter((~pl.col("true_condition")) & (pl.col("test_result"))).height
    fn = t_df.filter((pl.col("true_condition")) & (~pl.col("test_result"))).height
    prevalence = t_df.filter(pl.col("true_condition")).height / t_df.height

    # Check for potential division by zero
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    ppv = tp / (tp + fp) if (tp + fp) > 0 else 0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0

    likelihood_ratio_pos = sensitivity / (1 - specificity)
    likelihood_ratio_neg = (1 - sensitivity) / specificity

    pretest_odds = prevalence / (1 - prevalence)
    posttest_odds = pretest_odds * likelihood_ratio_pos

    pretest_prob = pretest_odds*100
    posttest_prob = posttest_odds / (posttest_odds + 1)


    accuracy = (tp + tn) / t_df.height if t_df.height > 0 else 0

    # Calculate confidence intervals
    n = t_df.height
    z = 1.96  # Assuming 95% confidence level

    # Sensitivity confidence interval
    sensitivity_se = math.sqrt((sensitivity * (1 - sensitivity)) / n)
    sensitivity_lower = sensitivity - z * sensitivity_se
    sensitivity_upper = sensitivity + z * sensitivity_se

    # Specificity confidence interval
    specificity_se = math.sqrt((specificity * (1 - specificity)) / n)
    specificity_lower = specificity - z * specificity_se
    specificity_upper = specificity + z * specificity_se

    # Accuracy confidence interval
    accuracy_se = math.sqrt((accuracy * (1 - accuracy)) / n)
    accuracy_lower = accuracy - z * accuracy_se
    accuracy_upper = accuracy + z * accuracy_se

    # Post-test probability confidence interval
    posttest_prob_lower = (posttest_prob - z * math.sqrt(posttest_prob * (1 - posttest_prob) / n))
    posttest_prob_upper = (posttest_prob + z * math.sqrt(posttest_prob * (1 - posttest_prob) / n))

    # messages += f"We tested for {condition} which has a prevalence of  {prevalence*100:.2f}% in this population\n\n"

    # messages += f"Pre-Test Probability: {pretest_odds*100:.2f}%\n\n"
    # messages += f"Post Test Probability: {posttest_prob*100:.2f}% (95% CI: {(posttest_prob - 1.96*math.sqrt(posttest_prob*(1-posttest_prob)/n))*100:.2f}%, {(posttest_prob + 1.96*math.sqrt(posttest_prob*(1-posttest_prob)/n))*100:.2f}%)\n"
    # messages += f"Percentage of people with a wrong result: {(1-accuracy)*100:.2f}% (95% CI: {(1-accuracy_upper)*100:.2f}%, {(1-accuracy_lower)*100:.2f}%)\n"

    metrics_dict = {
        "sensitivity": round(sensitivity*100, 2),
        "specificity": round(specificity*100, 2),
        "true_positives": tp,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "positive_predictive_value": round(ppv*100, 2),
        "negative_predictive_value": round(npv*100, 2), 
        "positive_likelihood_ratio": likelihood_ratio_pos,
        "negative_likelihood_ratio": likelihood_ratio_neg,
        "prevalence": prevalence,
        "pretest_odds": pretest_odds,
        "posttest_odds": posttest_odds,
        "pretest_probability": pretest_prob,
        "posttest_probability": posttest_prob,
        "accuracy": accuracy,
        "sensitivity_ci": (sensitivity_lower, sensitivity_upper),
        "specificity_ci": (specificity_lower, specificity_upper),
        "accuracy_ci": (accuracy_lower, accuracy_upper),
        "accuracy_se": accuracy_se,
        "sensitivity_se": sensitivity_se,
        "specificity_se": specificity_se,
        "post_test_probability_lower": posttest_prob_lower,
        "post_test_probability_upper": posttest_prob_upper,
    }
    return metrics_dict, messages
