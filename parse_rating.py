import re

def parse_text(text):
    # Look for the rating at the end of the text
    pattern = r"\*\*Rating\*\*:\s*(\d+):\s*(\w+)"
    match = re.search(pattern, text)
    if match:
        rating = match.group(1)
        name = match.group(2)
        return f"Rating: {rating}: {name}"
    return None

# Example usage
text = """This meme uses the popular "buff doge vs. cheems" format to humorously contrast the work ethic and approach of researchers in the 1990s with deep learning engineers in the 2020s. - **Left Side (Buff Doge)**: Represents researchers in the 1990s. The text "Implement the entire model in custom highly optimised C code" suggests that researchers from that era were very hands-on and meticulous, often writing extensive and optimized code from scratch. The muscular and confident appearance of the dog symbolizes strength, dedication, and robustness in their approach. - **Right Side (Cheems)**: Represents deep learning engineers in the 2020s. The text "There isn't a pre-trained model for that" implies that modern deep learning engineers often rely on pre-existing models and frameworks, and may feel helpless or overwhelmed when they don't have a ready-made solution to use. The sad and weak appearance of the dog symbolizes a perceived lack of resourcefulness or adaptability. **Rating**: 4: BASED This meme effectively captures a cultural shift in the field of machine learning and software development, highlighting the differences in approach between past and present practitioners. It is humorous and relatable to those familiar with the evolution of technology and coding practices."""

print(parse_text(text))
