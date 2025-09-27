import numpy as np

def map_severity(prob):
    if prob >= 0.85: return "Severe"
    elif prob >= 0.6: return "Moderate"
    elif prob >= 0.4: return "Mild"
    return "Low/Uncertain"

def combine_predictions(pred_list):
    """Average probabilities across multiple images"""
    avg_probs = np.mean(np.array(pred_list), axis=0)
    return avg_probs
