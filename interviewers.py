import ollama

def fetch_questions_from_ollama(job_role, interview_type, difficulty):
    """Fetches interview questions dynamically using Ollama"""
    prompt = f"Generate {difficulty.lower()} level {interview_type} questions for a {job_role} interview."

    response = ollama.chat(model="mistral", messages=[{"role": "system", "content": "You are an expert interviewer."},
                                                       {"role": "user", "content": prompt}])
    
    questions = response["message"]["content"].split("\n")
    return [q for q in questions if q.strip()]

# Example Usage:
# print(fetch_questions_from_ollama("Software Engineer", "Technical Interview", "Medium"))
