def parse_political_analysis(response):
    analysis = {
        'Left-Right': {'Score': None, 'Analysis': ''},
        'Libertarian-Authoritarian': {'Score': None, 'Analysis': ''}
    }
    
    # Split the response into parts
    parts = response.split("**")
    
    current_dimension = None
    for part in parts:
        if "Left-Right" in part:
            current_dimension = 'Left-Right'
        elif "Libertarian-Authoritarian" in part:
            current_dimension = 'Libertarian-Authoritarian'
        
        if current_dimension:
            score_str = part.split(":")[1].split("(")[0].strip()
            analysis[current_dimension]['Score'] = int(score_str) if score_str.isdigit() else None
            
            analysis_text = part.split("**Political Score:**")[1].strip() if "**Political Score:**" in part else ''
            analysis[current_dimension]['Analysis'] = analysis_text.split("**Query for X API")[0].strip()
    
    return analysis
