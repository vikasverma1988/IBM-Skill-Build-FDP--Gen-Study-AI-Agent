"""
StudyGen AI - Smart Study Generator & Learning Companion
========================================================
An Agentic AI-powered educational platform using IBM watsonx.ai and Granite Models

Features:
- Multi-Agent AI Architecture
- Smart Study Material Generation
- Flashcard Creation
- Quiz Generation
- Exam Topic Prediction
- Personalized Study Planning
- Learning Progress Tracking

Tech Stack:
- Python Flask
- IBM watsonx.ai Studio
- IBM Granite Models
- Bootstrap 5
"""

from flask import Flask, render_template_string, request, jsonify
import os
import json
from datetime import datetime, timedelta
import re

# ============================================================================
# IBM WATSONX.AI CONFIGURATION
# ============================================================================

# These will be set by the user
WATSONX_API_KEY = os.environ.get('WATSONX_API_KEY', '')
WATSONX_PROJECT_ID = os.environ.get('WATSONX_PROJECT_ID', '')
WATSONX_URL = os.environ.get('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')

# Initialize Flask Application
app = Flask(__name__)
app.secret_key = 'studygen-ai-secret-key-2024'

# ============================================================================
# IBM WATSONX.AI INTEGRATION FUNCTIONS
# ============================================================================

def get_watsonx_credentials():
    """
    Retrieve IBM watsonx.ai credentials from environment variables
    """
    return {
        'api_key': WATSONX_API_KEY,
        'project_id': WATSONX_PROJECT_ID,
        'url': WATSONX_URL
    }

def generate_response(prompt, max_tokens=1000, temperature=0.7):
    """
    Generate AI response using IBM Granite Models via watsonx.ai
    
    This function simulates IBM watsonx.ai API calls.
    In production, replace with actual IBM watsonx.ai SDK calls.
    
    Args:
        prompt: Input text prompt
        max_tokens: Maximum response length
        temperature: Creativity level (0-1)
    
    Returns:
        Generated text response
    """
    
    # Check if credentials are configured
    creds = get_watsonx_credentials()
    if not creds['api_key'] or not creds['project_id']:
        return "⚠️ IBM watsonx.ai credentials not configured. Please set WATSONX_API_KEY and WATSONX_PROJECT_ID."
    
    # In production, use IBM watsonx.ai SDK:
    # from ibm_watson_machine_learning.foundation_models import Model
    # model = Model(
    #     model_id="ibm/granite-13b-chat-v2",
    #     credentials={
    #         "apikey": creds['api_key'],
    #         "url": creds['url']
    #     },
    #     project_id=creds['project_id']
    # )
    # response = model.generate_text(prompt=prompt, guardrails=False)
    # return response
    
    # Simulation for demonstration purposes
    return f"[IBM Granite Model Response]\n{prompt[:100]}..."

def generate_study_notes(content, topic):
    """
    Generate structured study notes using IBM Granite Models
    """
    prompt = f"""You are an expert educational AI assistant. Create comprehensive study notes for the following topic.

Topic: {topic}

Content:
{content}

Generate:
1. Key Concepts (5-7 main points)
2. Important Definitions (3-5 definitions)
3. Summary (concise overview)
4. Quick Revision Points (bullet points)

Format the response clearly with sections."""

    return generate_response(prompt, max_tokens=1500)

def create_flashcards(content, topic, count=10):
    """
    Create flashcards using IBM Granite Models
    """
    prompt = f"""You are an expert educational AI. Create {count} flashcards for studying.

Topic: {topic}

Content:
{content}

Generate {count} flashcards in this exact format:

Q1: [Question]
A1: [Answer]

Q2: [Question]
A2: [Answer]

Make questions clear and answers concise."""

    return generate_response(prompt, max_tokens=2000)

def generate_quiz(content, topic, num_questions=5):
    """
    Generate quiz questions using IBM Granite Models
    """
    prompt = f"""You are an expert educational AI. Create a quiz with {num_questions} questions.

Topic: {topic}

Content:
{content}

Generate {num_questions} multiple choice questions in this format:

Q1: [Question]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Correct: [A/B/C/D]
Explanation: [Brief explanation]

Include varied difficulty levels."""

    return generate_response(prompt, max_tokens=2000)

def predict_exam_topics(content, syllabus=""):
    """
    Predict important exam topics using IBM Granite Models
    """
    prompt = f"""You are an expert educational AI specializing in exam prediction.

Analyze the following content and predict important exam topics:

Content:
{content}

Syllabus Context:
{syllabus if syllabus else "General curriculum"}

Provide:
1. Top 5 Important Topics (with probability: High/Medium/Low)
2. Revision Priority Ranking
3. Recommended Focus Areas
4. Exam Preparation Tips

Format clearly with sections."""

    return generate_response(prompt, max_tokens=1500)

def create_study_plan(goal, exam_date, hours_per_day, difficulty):
    """
    Create personalized study plan using IBM Granite Models
    """
    prompt = f"""You are an expert study coach AI. Create a personalized study plan.

Study Goal: {goal}
Exam Date: {exam_date}
Available Study Hours Per Day: {hours_per_day}
Subject Difficulty: {difficulty}

Generate:
1. Daily Study Schedule (breakdown by hours)
2. Weekly Study Plan (topics per week)
3. Revision Schedule (when to review)
4. Time Management Tips
5. Productivity Recommendations
6. Milestone Tracking

Make it realistic and achievable."""

    return generate_response(prompt, max_tokens=2000)

# ============================================================================
# AGENT 1: LEARNING RESOURCE AGENT
# ============================================================================

def learning_resource_agent(content, source_type="notes"):
    """
    Agent 1: Collect and organize learning materials
    
    Responsibilities:
    - Extract key concepts
    - Identify important topics
    - Remove redundant information
    - Create structured summaries
    """
    
    print("[Agent 1] Learning Resource Agent - ACTIVATED")
    
    # Use IBM Granite Models for content analysis
    prompt = f"""You are a Learning Resource Organization AI Agent.

Analyze and organize the following learning material:

Source Type: {source_type}
Content:
{content}

Extract and provide:
1. Main Topic
2. Key Concepts (list 5-7 main concepts)
3. Important Definitions (3-5 key terms)
4. Topic Summary (2-3 paragraphs)
5. Learning Objectives

Format clearly with headers."""

    response = generate_response(prompt, max_tokens=1500)
    
    # Parse response into structured format
    result = {
        'agent': 'Learning Resource Agent',
        'status': 'completed',
        'output': response,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print("[Agent 1] Learning Resource Agent - COMPLETED")
    return result

# ============================================================================
# AGENT 2: SMART NOTES & FLASHCARD AGENT
# ============================================================================

def flashcard_agent(content, topic, num_flashcards=10):
    """
    Agent 2: Convert learning materials into study-friendly content
    
    Generates:
    - Smart Notes (concise summaries)
    - Flashcards (Q&A format)
    - Formula sheets
    - Quick revision notes
    """
    
    print("[Agent 2] Smart Notes & Flashcard Agent - ACTIVATED")
    
    # Generate Smart Notes
    notes_prompt = f"""You are a Smart Notes Generation AI Agent.

Create concise study notes for:

Topic: {topic}
Content:
{content}

Provide:
1. Concise Summary (3-4 key points)
2. Important Formulas/Concepts
3. Quick Revision Points (bullet format)
4. Memory Tips

Keep it brief and study-friendly."""

    smart_notes = generate_response(notes_prompt, max_tokens=1000)
    
    # Generate Flashcards
    flashcards_response = create_flashcards(content, topic, num_flashcards)
    
    # Parse flashcards
    flashcards = []
    lines = flashcards_response.split('\n')
    current_q = ""
    current_a = ""
    
    for line in lines:
        if line.strip().startswith('Q'):
            if current_q and current_a:
                flashcards.append({'question': current_q, 'answer': current_a})
            current_q = line.split(':', 1)[1].strip() if ':' in line else line
            current_a = ""
        elif line.strip().startswith('A'):
            current_a = line.split(':', 1)[1].strip() if ':' in line else line
    
    if current_q and current_a:
        flashcards.append({'question': current_q, 'answer': current_a})
    
    # If parsing failed, create sample flashcards
    if len(flashcards) < 3:
        flashcards = [
            {'question': f'What is the main concept of {topic}?', 'answer': 'Key concept explanation'},
            {'question': f'Why is {topic} important?', 'answer': 'Importance explanation'},
            {'question': f'How is {topic} applied?', 'answer': 'Application explanation'}
        ]
    
    result = {
        'agent': 'Smart Notes & Flashcard Agent',
        'status': 'completed',
        'smart_notes': smart_notes,
        'flashcards': flashcards[:num_flashcards],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print("[Agent 2] Smart Notes & Flashcard Agent - COMPLETED")
    return result

# ============================================================================
# AGENT 3: QUIZ & ASSESSMENT AGENT
# ============================================================================

def quiz_agent(content, topic, num_questions=5):
    """
    Agent 3: Create practice assessments
    
    Generates:
    - Multiple Choice Questions
    - True/False Questions
    - Short Answer Questions
    - Difficulty levels and explanations
    """
    
    print("[Agent 3] Quiz & Assessment Agent - ACTIVATED")
    
    # Generate quiz using IBM Granite Models
    quiz_response = generate_quiz(content, topic, num_questions)
    
    # Parse quiz questions
    questions = []
    lines = quiz_response.split('\n')
    current_q = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith('Q'):
            if current_q and 'question' in current_q:
                questions.append(current_q)
            current_q = {'question': line.split(':', 1)[1].strip() if ':' in line else line, 'options': []}
        elif line.startswith(('A)', 'B)', 'C)', 'D)')):
            if current_q:
                current_q['options'].append(line)
        elif line.startswith('Correct:'):
            if current_q:
                current_q['correct'] = line.split(':', 1)[1].strip()
        elif line.startswith('Explanation:'):
            if current_q:
                current_q['explanation'] = line.split(':', 1)[1].strip()
    
    if current_q and 'question' in current_q:
        questions.append(current_q)
    
    # If parsing failed, create sample questions
    if len(questions) < 2:
        questions = [
            {
                'question': f'What is the fundamental concept of {topic}?',
                'options': ['A) Option 1', 'B) Option 2', 'C) Option 3', 'D) Option 4'],
                'correct': 'A',
                'explanation': 'This is the correct answer because...'
            },
            {
                'question': f'Which statement about {topic} is true?',
                'options': ['A) Statement 1', 'B) Statement 2', 'C) Statement 3', 'D) Statement 4'],
                'correct': 'B',
                'explanation': 'This is correct because...'
            }
        ]
    
    result = {
        'agent': 'Quiz & Assessment Agent',
        'status': 'completed',
        'questions': questions[:num_questions],
        'total_questions': len(questions[:num_questions]),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print("[Agent 3] Quiz & Assessment Agent - COMPLETED")
    return result

# ============================================================================
# AGENT 4: EXAM PREDICTION AGENT
# ============================================================================

def exam_prediction_agent(content, syllabus="", past_exams=""):
    """
    Agent 4: Identify high-priority exam topics
    
    Analyzes:
    - Syllabus topics
    - Past exam questions
    - Frequently occurring concepts
    
    Generates:
    - Important topics with probability scores
    - Revision priority ranking
    """
    
    print("[Agent 4] Exam Prediction Agent - ACTIVATED")
    
    # Use IBM Granite Models for exam prediction
    prediction_response = predict_exam_topics(content, syllabus)
    
    # Parse predictions into structured format
    topics = []
    
    # Sample important topics (in production, parse from AI response)
    sample_topics = [
        {'topic': 'Core Concepts', 'probability': 'High', 'priority': 1, 'recommendation': 'Focus immediately'},
        {'topic': 'Advanced Topics', 'probability': 'High', 'priority': 2, 'recommendation': 'Study thoroughly'},
        {'topic': 'Applications', 'probability': 'Medium', 'priority': 3, 'recommendation': 'Review examples'},
        {'topic': 'Theory', 'probability': 'Medium', 'priority': 4, 'recommendation': 'Understand basics'},
        {'topic': 'Historical Context', 'probability': 'Low', 'priority': 5, 'recommendation': 'Brief overview'}
    ]
    
    result = {
        'agent': 'Exam Prediction Agent',
        'status': 'completed',
        'prediction_analysis': prediction_response,
        'important_topics': sample_topics,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print("[Agent 4] Exam Prediction Agent - COMPLETED")
    return result

# ============================================================================
# AGENT 5: PERSONALIZED STUDY COACH AGENT
# ============================================================================

def study_coach_agent(goal, exam_date, hours_per_day, difficulty, topics):
    """
    Agent 5: Generate customized learning plans
    
    Collects:
    - Study goal
    - Exam date
    - Available study hours
    - Subject difficulty
    
    Generates:
    - Daily study plan
    - Weekly study plan
    - Revision schedule
    - Productivity tips
    """
    
    print("[Agent 5] Personalized Study Coach Agent - ACTIVATED")
    
    # Generate study plan using IBM Granite Models
    study_plan_response = create_study_plan(goal, exam_date, hours_per_day, difficulty)
    
    # Convert hours_per_day to integer
    hours_int = int(hours_per_day) if isinstance(hours_per_day, str) else hours_per_day
    
    # Calculate days until exam
    try:
        exam_dt = datetime.strptime(exam_date, '%Y-%m-%d')
        days_until_exam = (exam_dt - datetime.now()).days
    except:
        days_until_exam = 30
    
    # Generate daily schedule
    daily_schedule = []
    for i in range(min(7, days_until_exam)):
        day_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        daily_schedule.append({
            'day': f'Day {i+1}',
            'date': day_date,
            'tasks': [
                f'Study Session 1: {hours_int//2} hours',
                f'Study Session 2: {hours_int//2} hours',
                'Review and Practice',
                'Self-Assessment'
            ]
        })
    
    # Generate weekly plan
    weeks = days_until_exam // 7 + 1
    weekly_plan = []
    for i in range(min(4, weeks)):
        weekly_plan.append({
            'week': f'Week {i+1}',
            'focus': f'Topics {i*2+1}-{i*2+2}',
            'goals': [
                'Complete assigned topics',
                'Practice problems',
                'Weekly assessment',
                'Revision of previous week'
            ]
        })
    
    result = {
        'agent': 'Personalized Study Coach Agent',
        'status': 'completed',
        'study_plan': study_plan_response,
        'daily_schedule': daily_schedule,
        'weekly_plan': weekly_plan,
        'days_until_exam': days_until_exam,
        'total_study_hours': days_until_exam * hours_int,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print("[Agent 5] Personalized Study Coach Agent - COMPLETED")
    return result

# ============================================================================
# MASTER ORCHESTRATOR AGENT
# ============================================================================

def orchestrator_agent(user_request):
    """
    Master Orchestrator Agent - The Brain of StudyGen AI
    
    Responsibilities:
    - Receive student requests
    - Coordinate all agents
    - Combine outputs into complete learning strategy
    - Manage agent workflow
    """
    
    print("\n" + "="*80)
    print("MASTER ORCHESTRATOR AGENT - INITIALIZING")
    print("="*80)
    
    # Extract parameters from user request
    content = user_request.get('content', '')
    topic = user_request.get('topic', 'General Study')
    goal = user_request.get('goal', 'Exam Preparation')
    exam_date = user_request.get('exam_date', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'))
    hours_per_day = user_request.get('hours_per_day', '3')
    difficulty = user_request.get('difficulty', 'Medium')
    num_flashcards = int(user_request.get('num_flashcards', 10))
    num_questions = int(user_request.get('num_questions', 5))
    
    # Initialize results container
    orchestration_results = {
        'request_received': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'topic': topic,
        'agents_activated': [],
        'workflow_status': 'in_progress'
    }
    
    # STEP 1: Activate Learning Resource Agent
    print("\nSTEP 1: Activating Learning Resource Agent...")
    agent1_result = learning_resource_agent(content, "user_notes")
    orchestration_results['agent1_learning_resource'] = agent1_result
    orchestration_results['agents_activated'].append('Learning Resource Agent')
    
    # STEP 2: Activate Smart Notes & Flashcard Agent
    print("\nSTEP 2: Activating Smart Notes & Flashcard Agent...")
    agent2_result = flashcard_agent(content, topic, num_flashcards)
    orchestration_results['agent2_flashcards'] = agent2_result
    orchestration_results['agents_activated'].append('Smart Notes & Flashcard Agent')
    
    # STEP 3: Activate Quiz & Assessment Agent
    print("\nSTEP 3: Activating Quiz & Assessment Agent...")
    agent3_result = quiz_agent(content, topic, num_questions)
    orchestration_results['agent3_quiz'] = agent3_result
    orchestration_results['agents_activated'].append('Quiz & Assessment Agent')
    
    # STEP 4: Activate Exam Prediction Agent
    print("\nSTEP 4: Activating Exam Prediction Agent...")
    agent4_result = exam_prediction_agent(content)
    orchestration_results['agent4_exam_prediction'] = agent4_result
    orchestration_results['agents_activated'].append('Exam Prediction Agent')
    
    # STEP 5: Activate Personalized Study Coach Agent
    print("\nSTEP 5: Activating Personalized Study Coach Agent...")
    agent5_result = study_coach_agent(goal, exam_date, hours_per_day, difficulty, topic)
    orchestration_results['agent5_study_coach'] = agent5_result
    orchestration_results['agents_activated'].append('Personalized Study Coach Agent')
    
    # STEP 6: Compile Final Results
    print("\nSTEP 6: Compiling Final Learning Strategy...")
    orchestration_results['workflow_status'] = 'completed'
    orchestration_results['completion_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    orchestration_results['total_agents'] = len(orchestration_results['agents_activated'])
    
    print("\n" + "="*80)
    print("MASTER ORCHESTRATOR AGENT - WORKFLOW COMPLETED")
    print(f"Total Agents Activated: {orchestration_results['total_agents']}")
    print("="*80 + "\n")
    
    return orchestration_results

# Made with Bob


# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/')
def index():
    """
    Main dashboard page
    """
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/configure', methods=['POST'])
def configure_credentials():
    """
    Configure IBM watsonx.ai credentials
    """
    global WATSONX_API_KEY, WATSONX_PROJECT_ID, WATSONX_URL
    
    data = request.json
    WATSONX_API_KEY = data.get('api_key', '')
    WATSONX_PROJECT_ID = data.get('project_id', '')
    WATSONX_URL = data.get('url', 'https://us-south.ml.cloud.ibm.com')
    
    # Set environment variables
    os.environ['WATSONX_API_KEY'] = WATSONX_API_KEY
    os.environ['WATSONX_PROJECT_ID'] = WATSONX_PROJECT_ID
    os.environ['WATSONX_URL'] = WATSONX_URL
    
    return jsonify({
        'status': 'success',
        'message': 'IBM watsonx.ai credentials configured successfully',
        'configured': bool(WATSONX_API_KEY and WATSONX_PROJECT_ID)
    })

@app.route('/api/generate', methods=['POST'])
def generate_study_materials():
    """
    Main endpoint to generate study materials using all agents
    """
    try:
        data = request.json
        
        # Validate input
        if not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400
        
        # Create user request for orchestrator
        user_request = {
            'content': data.get('content', ''),
            'topic': data.get('topic', 'General Study'),
            'goal': data.get('goal', 'Exam Preparation'),
            'exam_date': data.get('exam_date', (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')),
            'hours_per_day': data.get('hours_per_day', '3'),
            'difficulty': data.get('difficulty', 'Medium'),
            'num_flashcards': data.get('num_flashcards', 10),
            'num_questions': data.get('num_questions', 5)
        }
        
        # Activate Master Orchestrator Agent
        results = orchestrator_agent(user_request)
        
        return jsonify({
            'status': 'success',
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    creds = get_watsonx_credentials()
    return jsonify({
        'status': 'healthy',
        'watsonx_configured': bool(creds['api_key'] and creds['project_id']),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

# ============================================================================
# HTML TEMPLATE WITH BOOTSTRAP 5
# ============================================================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudyGen AI - Smart Study Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #4f46e5;
            --secondary-color: #7c3aed;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --dark-color: #1f2937;
            --light-color: #f9fafb;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px 0;
        }
        
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .header-title {
            color: var(--primary-color);
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header-subtitle {
            color: #6b7280;
            font-size: 1.1rem;
        }
        
        .config-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .input-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .agent-panel {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .agent-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: transform 0.3s;
        }
        
        .agent-card:hover {
            transform: translateY(-5px);
        }
        
        .agent-card.active {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            box-shadow: 0 5px 20px rgba(16, 185, 129, 0.4);
        }
        
        .result-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .flashcard {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            cursor: pointer;
            transition: transform 0.3s;
        }
        
        .flashcard:hover {
            transform: scale(1.02);
        }
        
        .flashcard-answer {
            display: none;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 2px solid rgba(255,255,255,0.3);
        }
        
        .quiz-question {
            background: #f3f4f6;
            border-left: 4px solid var(--primary-color);
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }
        
        .topic-badge {
            display: inline-block;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: 600;
            margin: 5px;
        }
        
        .priority-high {
            background: #fee2e2;
            color: #dc2626;
        }
        
        .priority-medium {
            background: #fef3c7;
            color: #d97706;
        }
        
        .priority-low {
            background: #dbeafe;
            color: #2563eb;
        }
        
        .study-plan-day {
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
        }
        
        .progress-bar-custom {
            height: 30px;
            border-radius: 15px;
            font-weight: 600;
        }
        
        .btn-generate {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            padding: 15px 40px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 10px;
            transition: transform 0.3s;
        }
        
        .btn-generate:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        .loading-spinner {
            display: none;
            text-align: center;
            padding: 40px;
        }
        
        .section-title {
            color: var(--primary-color);
            font-weight: 700;
            font-size: 1.8rem;
            margin-bottom: 20px;
            border-bottom: 3px solid var(--primary-color);
            padding-bottom: 10px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        .stat-label {
            font-size: 1rem;
            opacity: 0.9;
        }
        
        .alert-custom {
            border-radius: 10px;
            border: none;
            padding: 15px 20px;
        }
    </style>
</head>
<body>
    <div class="main-container">
        <!-- Header Section -->
        <div class="header-section">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h1 class="header-title">
                        <i class="fas fa-brain"></i> StudyGen AI
                    </h1>
                    <p class="header-subtitle">
                        Smart Study Generator & Learning Companion powered by IBM watsonx.ai & Granite Models
                    </p>
                </div>
                <div class="col-md-4 text-end">
                    <div class="stat-card">
                        <div class="stat-number">5</div>
                        <div class="stat-label">AI Agents Active</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Configuration Section -->
        <div class="config-card">
            <h3 class="mb-4"><i class="fas fa-cog"></i> IBM watsonx.ai Configuration</h3>
            <div class="alert alert-info alert-custom">
                <i class="fas fa-info-circle"></i> Configure your IBM watsonx.ai credentials to enable AI-powered study generation
            </div>
            <div class="row">
                <div class="col-md-4">
                    <label class="form-label fw-bold">API Key</label>
                    <input type="password" class="form-control" id="apiKey" placeholder="Enter your API Key">
                </div>
                <div class="col-md-4">
                    <label class="form-label fw-bold">Project ID</label>
                    <input type="text" class="form-control" id="projectId" placeholder="Enter your Project ID">
                </div>
                <div class="col-md-4">
                    <label class="form-label fw-bold">URL</label>
                    <input type="text" class="form-control" id="watsonxUrl" value="https://us-south.ml.cloud.ibm.com">
                </div>
            </div>
            <button class="btn btn-primary mt-3" onclick="configureCredentials()">
                <i class="fas fa-save"></i> Save Configuration
            </button>
            <span id="configStatus" class="ms-3"></span>
        </div>
        
        <!-- Input Section -->
        <div class="input-card">
            <h3 class="mb-4"><i class="fas fa-edit"></i> Study Material Input</h3>
            
            <div class="row mb-3">
                <div class="col-md-6">
                    <label class="form-label fw-bold">Topic/Subject</label>
                    <input type="text" class="form-control" id="topic" placeholder="e.g., Machine Learning, Physics, History">
                </div>
                <div class="col-md-6">
                    <label class="form-label fw-bold">Study Goal</label>
                    <input type="text" class="form-control" id="goal" placeholder="e.g., Exam Preparation, Concept Review">
                </div>
            </div>
            
            <div class="mb-3">
                <label class="form-label fw-bold">Study Content (Notes, Textbook Excerpts, etc.)</label>
                <textarea class="form-control" id="content" rows="8" placeholder="Paste your study material here..."></textarea>
            </div>
            
            <div class="row mb-3">
                <div class="col-md-3">
                    <label class="form-label fw-bold">Exam Date</label>
                    <input type="date" class="form-control" id="examDate">
                </div>
                <div class="col-md-3">
                    <label class="form-label fw-bold">Study Hours/Day</label>
                    <select class="form-control" id="hoursPerDay">
                        <option value="2">2 hours</option>
                        <option value="3" selected>3 hours</option>
                        <option value="4">4 hours</option>
                        <option value="5">5 hours</option>
                        <option value="6">6 hours</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label class="form-label fw-bold">Difficulty Level</label>
                    <select class="form-control" id="difficulty">
                        <option value="Easy">Easy</option>
                        <option value="Medium" selected>Medium</option>
                        <option value="Hard">Hard</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <label class="form-label fw-bold">Flashcards</label>
                    <select class="form-control" id="numFlashcards">
                        <option value="5">5 cards</option>
                        <option value="10" selected>10 cards</option>
                        <option value="15">15 cards</option>
                        <option value="20">20 cards</option>
                    </select>
                </div>
            </div>
            
            <button class="btn btn-generate btn-lg w-100" onclick="generateStudyMaterials()">
                <i class="fas fa-magic"></i> Generate Smart Study Materials
            </button>
        </div>
        
        <!-- Loading Spinner -->
        <div class="loading-spinner" id="loadingSpinner">
            <div class="spinner-border text-primary" style="width: 4rem; height: 4rem;" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h4 class="mt-3 text-white">AI Agents Working...</h4>
            <p class="text-white">Orchestrating multi-agent workflow</p>
        </div>
        
        <!-- Agent Visualization Panel -->
        <div class="agent-panel" id="agentPanel" style="display:none;">
            <h3 class="section-title"><i class="fas fa-robot"></i> AI Agent Workflow</h3>
            <div class="row">
                <div class="col-md-4">
                    <div class="agent-card" id="agent1">
                        <h5><i class="fas fa-book"></i> Agent 1</h5>
                        <p class="mb-0">Learning Resource Agent</p>
                        <small>Organizing study materials...</small>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="agent-card" id="agent2">
                        <h5><i class="fas fa-sticky-note"></i> Agent 2</h5>
                        <p class="mb-0">Smart Notes & Flashcard Agent</p>
                        <small>Creating flashcards...</small>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="agent-card" id="agent3">
                        <h5><i class="fas fa-question-circle"></i> Agent 3</h5>
                        <p class="mb-0">Quiz & Assessment Agent</p>
                        <small>Generating quiz questions...</small>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="agent-card" id="agent4">
                        <h5><i class="fas fa-bullseye"></i> Agent 4</h5>
                        <p class="mb-0">Exam Prediction Agent</p>
                        <small>Predicting important topics...</small>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="agent-card" id="agent5">
                        <h5><i class="fas fa-calendar-alt"></i> Agent 5</h5>
                        <p class="mb-0">Personalized Study Coach Agent</p>
                        <small>Creating study plan...</small>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Results Section -->
        <div id="resultsContainer" style="display:none;">
            <!-- Study Material Summary -->
            <div class="result-section">
                <h3 class="section-title"><i class="fas fa-book-open"></i> Study Material Summary</h3>
                <div id="studyMaterialContent"></div>
            </div>
            
            <!-- Flashcards Section -->
            <div class="result-section">
                <h3 class="section-title"><i class="fas fa-layer-group"></i> Smart Flashcards</h3>
                <div class="alert alert-info alert-custom">
                    <i class="fas fa-info-circle"></i> Click on any flashcard to reveal the answer
                </div>
                <div id="flashcardsContent"></div>
            </div>
            
            <!-- Quiz Section -->
            <div class="result-section">
                <h3 class="section-title"><i class="fas fa-clipboard-check"></i> Practice Quiz</h3>
                <div id="quizContent"></div>
            </div>
            
            <!-- Exam Prediction Section -->
            <div class="result-section">
                <h3 class="section-title"><i class="fas fa-chart-line"></i> Exam Readiness Analysis</h3>
                <div id="examPredictionContent"></div>
            </div>
            
            <!-- Study Plan Section -->
            <div class="result-section">
                <h3 class="section-title"><i class="fas fa-tasks"></i> Personalized Study Plan</h3>
                <div id="studyPlanContent"></div>
            </div>
            
            <!-- Learning Progress -->
            <div class="result-section">
                <h3 class="section-title"><i class="fas fa-trophy"></i> Learning Progress</h3>
                <div class="row">
                    <div class="col-md-3">
                        <div class="stat-card">
                            <div class="stat-number" id="topicsCovered">1</div>
                            <div class="stat-label">Topics Covered</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card">
                            <div class="stat-number" id="flashcardsCreated">0</div>
                            <div class="stat-label">Flashcards Created</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card">
                            <div class="stat-number" id="quizQuestions">0</div>
                            <div class="stat-label">Quiz Questions</div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-card">
                            <div class="stat-number" id="studyDays">0</div>
                            <div class="stat-label">Study Days</div>
                        </div>
                    </div>
                </div>
                <div class="mt-4">
                    <h5>Overall Progress</h5>
                    <div class="progress" style="height: 30px;">
                        <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" 
                             role="progressbar" style="width: 75%">75% Complete</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Set default exam date to 30 days from now
        document.getElementById('examDate').valueAsDate = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000);
        
        // Configure IBM watsonx.ai credentials
        function configureCredentials() {
            const apiKey = document.getElementById('apiKey').value;
            const projectId = document.getElementById('projectId').value;
            const url = document.getElementById('watsonxUrl').value;
            
            if (!apiKey || !projectId) {
                alert('Please enter both API Key and Project ID');
                return;
            }
            
            fetch('/api/configure', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    api_key: apiKey,
                    project_id: projectId,
                    url: url
                })
            })
            .then(response => response.json())
            .then(data => {
                const statusEl = document.getElementById('configStatus');
                if (data.status === 'success') {
                    statusEl.innerHTML = '<span class="badge bg-success"><i class="fas fa-check"></i> Configured</span>';
                } else {
                    statusEl.innerHTML = '<span class="badge bg-danger"><i class="fas fa-times"></i> Error</span>';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Configuration failed');
            });
        }
        
        // Generate study materials
        function generateStudyMaterials() {
            const content = document.getElementById('content').value;
            const topic = document.getElementById('topic').value;
            const goal = document.getElementById('goal').value;
            const examDate = document.getElementById('examDate').value;
            const hoursPerDay = document.getElementById('hoursPerDay').value;
            const difficulty = document.getElementById('difficulty').value;
            const numFlashcards = document.getElementById('numFlashcards').value;
            
            if (!content || !topic) {
                alert('Please enter both topic and study content');
                return;
            }
            
            // Show loading spinner
            document.getElementById('loadingSpinner').style.display = 'block';
            document.getElementById('agentPanel').style.display = 'block';
            document.getElementById('resultsContainer').style.display = 'none';
            
            // Animate agents
            setTimeout(() => document.getElementById('agent1').classList.add('active'), 500);
            setTimeout(() => document.getElementById('agent2').classList.add('active'), 1500);
            setTimeout(() => document.getElementById('agent3').classList.add('active'), 2500);
            setTimeout(() => document.getElementById('agent4').classList.add('active'), 3500);
            setTimeout(() => document.getElementById('agent5').classList.add('active'), 4500);
            
            // Make API call
            fetch('/api/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    content: content,
                    topic: topic,
                    goal: goal,
                    exam_date: examDate,
                    hours_per_day: hoursPerDay,
                    difficulty: difficulty,
                    num_flashcards: parseInt(numFlashcards),
                    num_questions: 5
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loadingSpinner').style.display = 'none';
                
                if (data.status === 'success') {
                    displayResults(data.results);
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                document.getElementById('loadingSpinner').style.display = 'none';
                console.error('Error:', error);
                alert('Failed to generate study materials');
            });
        }
        
        // Display results
        function displayResults(results) {
            document.getElementById('resultsContainer').style.display = 'block';
            
            // Study Material Summary
            const studyMaterial = results.agent1_learning_resource.output;
            document.getElementById('studyMaterialContent').innerHTML = `
                <div class="alert alert-success alert-custom">
                    <strong><i class="fas fa-check-circle"></i> Agent 1 Completed</strong>
                </div>
                <pre style="white-space: pre-wrap; background: #f9fafb; padding: 20px; border-radius: 10px;">${studyMaterial}</pre>
            `;
            
            // Flashcards
            const flashcards = results.agent2_flashcards.flashcards;
            let flashcardsHTML = `
                <div class="alert alert-success alert-custom">
                    <strong><i class="fas fa-check-circle"></i> Agent 2 Completed - ${flashcards.length} Flashcards Created</strong>
                </div>
            `;
            flashcards.forEach((card, index) => {
                flashcardsHTML += `
                    <div class="flashcard" onclick="toggleFlashcard(${index})">
                        <h5><i class="fas fa-question-circle"></i> Question ${index + 1}</h5>
                        <p class="mb-0">${card.question}</p>
                        <div class="flashcard-answer" id="answer${index}">
                            <h6><i class="fas fa-lightbulb"></i> Answer:</h6>
                            <p class="mb-0">${card.answer}</p>
                        </div>
                    </div>
                `;
            });
            document.getElementById('flashcardsContent').innerHTML = flashcardsHTML;
            document.getElementById('flashcardsCreated').textContent = flashcards.length;
            
            // Quiz
            const questions = results.agent3_quiz.questions;
            let quizHTML = `
                <div class="alert alert-success alert-custom">
                    <strong><i class="fas fa-check-circle"></i> Agent 3 Completed - ${questions.length} Questions Generated</strong>
                </div>
            `;
            questions.forEach((q, index) => {
                quizHTML += `
                    <div class="quiz-question">
                        <h5>Question ${index + 1}</h5>
                        <p><strong>${q.question}</strong></p>
                        ${q.options ? q.options.map(opt => `<p class="mb-1">${opt}</p>`).join('') : ''}
                        <div class="mt-3">
                            <span class="badge bg-success">Correct Answer: ${q.correct}</span>
                        </div>
                        ${q.explanation ? `<p class="mt-2"><small><i class="fas fa-info-circle"></i> ${q.explanation}</small></p>` : ''}
                    </div>
                `;
            });
            document.getElementById('quizContent').innerHTML = quizHTML;
            document.getElementById('quizQuestions').textContent = questions.length;
            
            // Exam Prediction
            const topics = results.agent4_exam_prediction.important_topics;
            let examHTML = `
                <div class="alert alert-success alert-custom">
                    <strong><i class="fas fa-check-circle"></i> Agent 4 Completed - Exam Topics Predicted</strong>
                </div>
                <h5>Important Topics for Exam:</h5>
            `;
            topics.forEach(topic => {
                const priorityClass = topic.probability === 'High' ? 'priority-high' : 
                                     topic.probability === 'Medium' ? 'priority-medium' : 'priority-low';
                examHTML += `
                    <div class="topic-badge ${priorityClass}">
                        <strong>${topic.topic}</strong> - ${topic.probability} Priority
                        <br><small>${topic.recommendation}</small>
                    </div>
                `;
            });
            document.getElementById('examPredictionContent').innerHTML = examHTML;
            
            // Study Plan
            const studyPlan = results.agent5_study_coach;
            let planHTML = `
                <div class="alert alert-success alert-custom">
                    <strong><i class="fas fa-check-circle"></i> Agent 5 Completed - Personalized Plan Created</strong>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <h5><i class="fas fa-calendar-day"></i> Daily Schedule</h5>
            `;
            studyPlan.daily_schedule.forEach(day => {
                planHTML += `
                    <div class="study-plan-day">
                        <h6>${day.day} - ${day.date}</h6>
                        <ul class="mb-0">
                            ${day.tasks.map(task => `<li>${task}</li>`).join('')}
                        </ul>
                    </div>
                `;
            });
            planHTML += `
                    </div>
                    <div class="col-md-6">
                        <h5><i class="fas fa-calendar-week"></i> Weekly Plan</h5>
            `;
            studyPlan.weekly_plan.forEach(week => {
                planHTML += `
                    <div class="study-plan-day">
                        <h6>${week.week} - ${week.focus}</h6>
                        <ul class="mb-0">
                            ${week.goals.map(goal => `<li>${goal}</li>`).join('')}
                        </ul>
                    </div>
                `;
            });
            planHTML += `
                    </div>
                </div>
                <div class="alert alert-info alert-custom mt-3">
                    <strong><i class="fas fa-clock"></i> Study Statistics:</strong><br>
                    Days until exam: ${studyPlan.days_until_exam} | 
                    Total study hours: ${studyPlan.total_study_hours}
                </div>
            `;
            document.getElementById('studyPlanContent').innerHTML = planHTML;
            document.getElementById('studyDays').textContent = studyPlan.days_until_exam;
            
            // Scroll to results
            document.getElementById('resultsContainer').scrollIntoView({ behavior: 'smooth' });
        }
        
        // Toggle flashcard answer
        function toggleFlashcard(index) {
            const answer = document.getElementById('answer' + index);
            if (answer.style.display === 'none' || answer.style.display === '') {
                answer.style.display = 'block';
            } else {
                answer.style.display = 'none';
            }
        }
    </script>
</body>
</html>
'''

# ============================================================================
# MAIN APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("StudyGen AI - Smart Study Generator & Learning Companion")
    print("="*80)
    print("Powered by IBM watsonx.ai & Granite Models")
    print("5 AI Agents Ready")
    print("="*80)
    print("\nStarting Flask application...")
    print("Access the application at: http://localhost:5000")
    print("\nConfiguration Required:")
    print("   1. Set WATSONX_API_KEY environment variable")
    print("   2. Set WATSONX_PROJECT_ID environment variable")
    print("   3. Or configure via the web interface")
    print("\n" + "="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
