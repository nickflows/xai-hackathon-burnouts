def parse_political_analysis(response):
    analysis = {
        'Left-Right': {'Score': None, 'Analysis': ''},
        'Libertarian-Authoritarian': {'Score': None, 'Analysis': ''}
    }

    # Check if 'Left-Right' and 'Libertarian-Authoritarian' are in the response
    if "Left-Right" in response:
        try:
            # Extract the Left-Right part
            left_right_part = response.split("**Left-Right:**")[1].split("- **Libertarian-Authoritarian:**")[0].strip()
            # Extract the score and the analysis
            left_right_score = int(left_right_part.split("(")[0].strip())
            left_right_analysis = left_right_part.split("(")[1].split(")")[0].strip()

            # Update the analysis dictionary
            analysis['Left-Right']['Score'] = left_right_score
            analysis['Left-Right']['Analysis'] = left_right_analysis
        except (IndexError, ValueError):
            # Handle any parsing errors
            analysis['Left-Right']['Analysis'] = "Parsing error for Left-Right analysis."

    if "Libertarian-Authoritarian" in response:
        try:
            # Extract the Libertarian-Authoritarian part
            libertarian_authoritarian_part = response.split("- **Libertarian-Authoritarian:**")[1].split("**Query for X API:**")[0].strip()
            # Extract the score and the analysis
            libertarian_authoritarian_score = int(libertarian_authoritarian_part.split("(")[0].strip())
            libertarian_authoritarian_analysis = libertarian_authoritarian_part.split("(")[1].split(")")[0].strip()

            # Update the analysis dictionary
            analysis['Libertarian-Authoritarian']['Score'] = libertarian_authoritarian_score
            analysis['Libertarian-Authoritarian']['Analysis'] = libertarian_authoritarian_analysis
        except (IndexError, ValueError):
            # Handle any parsing errors
            analysis['Libertarian-Authoritarian']['Analysis'] = "Parsing error for Libertarian-Authoritarian analysis."
    
    return analysis


