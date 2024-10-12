def parse_political_analysis(response):
    analysis = {}
    
    # Split the response into parts
    parts = response.split("**")
    
    # Extract Political Dimension and Score
    for part in parts:
        if "Left-Right" in part:
            analysis['Political Dimension'] = 'Left-Right'
            analysis['Score'] = int(part.split(":")[1].split("(")[0].strip())
        elif "Libertarian-Authoritarian" in part:
            analysis['Political Dimension'] = 'Libertarian-Authoritarian'
            analysis['Score'] = int(part.split(":")[1].split("(")[0].strip())
    
    # Extract Analysis
    analysis_text = response.split("**X API Query for Opposite Spectrum:**")[0]
    analysis['Analysis'] = analysis_text.split("**Political Score:**")[1].strip()
    
    return analysis

# Example usage
response = "**Political Score:** - **Left-Right:** 3 (The mention of social security, which is often supported by left-leaning individuals, suggests a more left-leaning perspective.) - **Libertarian-Authoritarian:** 6 (While the statement doesn't directly indicate authoritarianism, the reliance on government programs like social security can be seen as a slight lean towards authoritarianism in terms of government intervention in personal welfare.) **X API Query for Opposite Spectrum:** ```plaintext q=(\"I believe in personal responsibility\" OR \"government should not provide welfare\" OR \"social security is unsustainable\") lang:en -is:retweet ```"
parsed_analysis = parse_political_analysis(response)
print(parsed_analysis)
