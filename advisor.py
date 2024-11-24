import google.generativeai as genai
import os
from typing import Dict

class LegalCaseAnalyzer:
    def __init__(self):
        """Initialize the Google Gemini model with the API key."""
        api_key = "AIzaSyAEuC2MmuM83A-LsCffx5FoMwhmgGkadus"  # Replace with your actual API key

        # Configure the Gemini API client with the API key
        genai.configure(api_key=api_key)

        # Initialize both models
        self.model_flash = genai.GenerativeModel("gemini-1.5-flash")
        self.model_pro = genai.GenerativeModel("gemini-1.5-pro-002")

    def analyze_case(self, case_description: str) -> Dict:
        """Analyze a legal case by combining responses from two models for a comprehensive output."""

        prompt = f"""You are a seasoned legal expert tasked with providing an extensive, structured breakdown of arguments for both the plaintiff's and the defendant's advocates in a high level of debate between 2 senior lawyer in high court, and provided section in both ipc and bns . This analysis should be detailed, using legal reasoning suitable for those without legal representation, and should provide insightful guidance.

For 3 round of argument between the plaintiff's and the defendant's advocates, provide the following structured details for each side in atleast 5 points for each structured details, specially for supporting evidence and section and act:

1. **Legal Claims and Defenses**:
   - Outline the primary legal claims, defenses, and rights each side is asserting.
   - Reference relevant acts, laws, and sections that support each argument.
   - Ensure each claim or defense is well-explained to clarify its legal standing.

2. **Supporting Evidence and its Relevance**:
   - List and describe specific types of evidence (e.g., witness testimony, physical evidence, digital records) that support each claim or defense.
   - Explain how each piece of evidence strengthens the advocate's position and its potential impact on the court’s perspective.

3. **Landmark Judgments and Precedents**:
   - Include 5-8 high-profile judgments and legal precedents from similar cases.
   - For each precedent, provide a brief summary and explain its relevance to the current case.
   - Discuss how these judgments support the advocate's argument or establish a relevant legal principle.

4. **Counterarguments and Rebuttals**:
   - Respond directly to the opposing advocate’s points, addressing weaknesses or inconsistencies in their claims.
   - Use legal principles or evidence to counter the other side’s arguments effectively.

5. **Potential Legal Outcomes and Consequences**:
   - Describe the legal consequences and possible outcomes if each side’s arguments are upheld.
   - Discuss both immediate legal implications (e.g., penalties, fines) and long-term consequences (e.g., criminal records, civil liabilities).

Each advocate should respond directly to the previous argument made by the opposing side, attempting to refute or strengthen their case with additional points. Ensure that each round of argument is detailed, precise, and labeled clearly.

Case Description:
{case_description}

Please ensure the analysis is comprehensive and structured, offering a full view of the strengths and weaknesses of each side’s case through a high level of debate between 2 senior lawyer in high court. Present the arguments in a way that is both educational and actionable for someone without legal representation."""

        try:
            # Generate content using the flash model
            response_flash = self.model_flash.generate_content(prompt)
            flash_text = response_flash.text.strip() if response_flash.text else "No response from flash model."

            # Generate content using the pro model
            response_pro = self.model_pro.generate_content(prompt)
            pro_text = response_pro.text.strip() if response_pro.text else "No response from pro model."

            # Combine the results (e.g., concatenate or structure in rounds)
            combined_analysis = f"=== Analysis from gemini-1.5-flash ===\n{flash_text}\n\n=== Analysis from gemini-1.5-pro-002 ===\n{pro_text}"

            # Return the combined analysis
            return {"analysis": combined_analysis}

        except Exception as e:
            return {"error": f"Error in analyzing case: {str(e)}"}

def main():
    """Main function to run the legal analysis."""
    analyzer = LegalCaseAnalyzer()

    print("\n=== Legal Case Analysis System ===")
    print("\nPlease enter the case details below (press Enter twice when finished):\n")

    # Collect multiline input for case description
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        elif lines:  # Exit on empty line if we have content
            break

    case_description = '\n'.join(lines)

    print("\nAnalyzing case...")
    results = analyzer.analyze_case(case_description)

    if "error" in results:
        print(f"\nError: {results['error']}")
    else:
        print("\n=== Analysis Results ===\n")
        print(results["analysis"])

if __name__ == "__main__":
    main()
