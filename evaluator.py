import ollama
import random

def evaluate_interview(questions, answers):
    feedback = []
    total_score = 0
    
    for question, answer in zip(questions, answers):
        if answer.strip():
            score = random.randint(60, 100)  # Simulating AI scoring (replace with actual logic)
            feedback.append(f"✅ **{question}**\nScore: {score}/100\nFeedback: Good response.")
        else:
            score = 40  # Low score for unanswered questions
            feedback.append(f"❌ **{question}**\nScore: {score}/100\nFeedback: Answer was missing.")
        
        total_score += score

    avg_score = total_score / len(questions) if questions else 0
    return "\n\n".join(feedback), avg_score

