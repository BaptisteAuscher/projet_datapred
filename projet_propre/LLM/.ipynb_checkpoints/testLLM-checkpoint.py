from transformers import pipeline

fill_mask = pipeline(
    "fill-mask",
    model="google/electra-small-generator",
    tokenizer="google/electra-small-generator"
)

""" example :
print(
    fill_mask("Paris is the [MASK] of France.")
)"""

def scores_to_dict(results):
    score_dict = {}
    for result in results:
        score_dict[result['token_str']] = result['score']
    return score_dict

print(scores_to_dict(fill_mask("A targeted cyberattack on a key energy network has led to a sharp increase in energy costs \
                               across affected areas. The disruption to critical systems has prompted concerns over supply \
                               shortages and raised alarms about the vulnerability of infrastructure to cyber threats. \
                               Efforts to restore normalcy are underway, but consumers are already feeling the pinch with \
                               higher energy bills looming on the horizon. the previous text says that the cost of [MASK] \
                               will be affected.")))