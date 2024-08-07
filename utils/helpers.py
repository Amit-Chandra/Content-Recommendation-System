def get_top_recommendations(recommendations, top_n=5):
    """
    Get top N recommendations based on similarity score.

    Args:
    - recommendations (list of dict): List of recommendation items with 'similarity_score'.
    - top_n (int): Number of top recommendations to return.

    Returns:
    - list of dict: Top N recommendations sorted by similarity score.
    """
    if not recommendations:
        return []

    sorted_recommendations = sorted(recommendations, key=lambda x: x['similarity_score'], reverse=True)
    
    return sorted_recommendations[:min(top_n, len(sorted_recommendations))]
