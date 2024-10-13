def parse_text(text):
    import re
    pattern = r"Rating: (\d+): (\w+)"
    match = re.search(pattern, text)
    if match:
        rating = match.group(1)
        name = match.group(2)
        return f"Rating: {rating}: {name}"
    return None

# Example usage
text = """This meme is a humorous take on the idea of ChatGPT, an AI language model, winning the Nobel Prize in Literature. The image mimics the official announcement style of the Nobel Prize, complete with a formal portrait and a citation. The citation humorously states that ChatGPT won "for his intricate tapestry of prose which showcases the redundancy of sentience in art," poking fun at the AI's ability to generate text that can sometimes be overly complex or redundant, and questioning the role of human creativity in art. The humor lies in the absurdity of an AI winning a prestigious literary award, which is traditionally given to human authors for their contributions to literature. The phrase "redundancy of sentience in art" is a playful jab at how AI-generated content might lack the genuine human experience and emotion that typically characterizes great literature. Rating: 2: BASED This meme is clever and well-executed, making a humorous point about AI and literature without being overly biased."""
print(parse_text(text))
