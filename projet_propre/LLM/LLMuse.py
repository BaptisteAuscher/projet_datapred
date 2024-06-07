from transformers import pipeline
import numpy as np

fill_mask = pipeline(
    "fill-mask",
    model="google/electra-small-generator",
    tokenizer="google/electra-small-generator"
)

def scores_to_dict(results) :
    score_dict = {}
    for result in results:
        score_dict[result['token_str']] = result['score']
    return score_dict

def key_of_max_value(d) :
    max_key = None
    max_value = -1
    for key, value in d.items():
        if value > max_value:
            max_value = value
            max_key = key
    return max_key

# How much a given parameter it is going to be affected
def importance(text, parameter) :
    """
    Use google/electra-small-generator to get how much a given parameter is going to be affected according to the article. 
    example of parameter : cost of lithium
    """
    dict_result = scores_to_dict(fill_mask(text + f"the previous text says that the {parameter} will be affected. The {parameter} will tend to [MASK]."))
    trend = key_of_max_value(dict_result)
    trend_importance = dict_result[trend]
    return [trend, trend_importance]

# We summuarize it all
def text_to_trend(text, limit=0.025) :
    # We get what is going to be affected according to the article
    variables = dict()
    # cost 
    variables_from_text = scores_to_dict(fill_mask(text + "the previous text says that the cost of [MASK] will be affected."))
    for variable in variables_from_text :
        variables[f"cost of {variable}"] = variables_from_text[variable] 
    # Demand 
    variables_from_text = scores_to_dict(fill_mask(text + "the previous text says that the demand for [MASK] will be affected."))
    for variable in variables_from_text :
        variables[f"demand for {variable}"] = variables_from_text[variable] 
    # Available ressources
    variables_from_text = scores_to_dict(fill_mask(text + "the previous text says that the the available resource in [MASK] will be affected."))
    for variable in variables_from_text :
        variables[f"available resource in {variable}"] = variables_from_text[variable] 
    # Getting the importance of every trend
    result = dict()
    for parameter in variables :
        result[parameter] = importance(text, parameter)
        result[parameter][1] = result[parameter][1] * variables[parameter]
    # Keeping only what's relevant
    filtered_result = dict()
    for parameter in result :
        if result[parameter][1] > limit :
            filtered_result[parameter] = result[parameter]
    return filtered_result

# The input article
# text = "A targeted cyberattack on a key energy network has led to a sharp increase in energy costs across affected areas. The disruption to critical systems has prompted concerns over supply shortages and raised alarms about the vulnerability of infrastructure to cyber threats. Efforts to restore normalcy are underway, but consumers are already feeling the pinch with higher energy bills looming on the horizon."
# print(text_to_trend(text))

