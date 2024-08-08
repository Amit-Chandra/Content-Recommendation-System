def get_top_recommendations(recommendations, top_n=5):
    sorted_recommendations = sorted(recommendations, key=lambda x: x['similarity_score'], reverse=True)
    return sorted_recommendations[:top_n]

def remove_duplicates(recommendations):
    seen = set()
    unique_recommendations = []
    for rec in recommendations:
        if rec['video_id'] not in seen:
            seen.add(rec['video_id'])
            unique_recommendations.append(rec)
    return unique_recommendations

