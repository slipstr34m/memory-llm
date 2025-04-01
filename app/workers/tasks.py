from celery import shared_task
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
from app.config import PG_CONN_URL
from app.redis_client import redis_client
from openai import AzureOpenAI
from app.config import OPENAI_API_ENDPOINT, OPENAI_API_KEY

# Initialize OpenAI client (assuming you have an existing method for this)
openai_client = AzureOpenAI(
    azure_endpoint=OPENAI_API_ENDPOINT,
    api_key=OPENAI_API_KEY,
    api_version="2024-10-21"
)

def generate_user_profile(interview_text: str, existing_timeline: str = "None") -> str:
    """Generates an updated user profile timeline from interview transcripts."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""
    You are an expert biographer. Extract and summarize the most important details about the individual's psychology, behavior, experiences, and ambitions.
    Make sure to support every conclusion with specific citations.
    Below is the existing timeline of user profile updates. Do not modify past entries. Instead, append a new entry that references past insights and tracks any changes over time.

    Existing Timeline:
    {existing_timeline}

    New Interview Transcript:
    {interview_text}

    Respond with the updated timeline in the following format:

    -----
    [Timestamp: {timestamp}]
    Name: <Full Name>
    Psychological Makeup: <Updated personality traits, motivations, anxieties, cognitive biases>
    Behavioral Patterns: <New or evolved behaviors, decision-making styles, interpersonal tendencies>
    Significant Life Events: <New major experiences and their impact>
    Professional Aspirations: <Career progress, mindset changes, and work ethic evolution>
    Social and Family Influences: <Relationships that changed, new mentors, or evolving family dynamics>
    Additional Notes: <New insights, contradictions, or psychological patterns>
    -----
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()


@shared_task
def process_new_interviews():
    """Fetch new interviews from the last minute, generate profiles, and store them in Redis."""
    # Step 1: Connect to PostgreSQL and fetch interviews from the last minute
    conn = psycopg2.connect(PG_CONN_URL)
    query = """
        SELECT user_id, transcript, created_at
        FROM grapevine_aiinterviewinstance
        WHERE created_at >= %s
        ORDER BY created_at ASC;
    """
    
    # Get the timestamp for 1 minute ago
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    one_minute_ago_str = one_minute_ago.strftime('%Y-%m-%d %H:%M:%S')

    # Fetch the data using pandas
    df = pd.read_sql(query, conn, params=(one_minute_ago_str,))

    if df.empty:
        return "No new interviews found in the last minute."

    # Step 2: Process each interview and generate a profile timeline for each user
    user_groups = df.groupby("user_id")

    for user_id, user_interviews in user_groups:
        # Step 3: Fetch all interviews for the user (in chronological order)
        query_all_user_interviews = """
            SELECT transcript
            FROM grapevine_aiinterviewinstance
            WHERE user_id = %s
            ORDER BY created_at ASC
            LIMIT 5;
        """
        user_interviews_df = pd.read_sql(query_all_user_interviews, conn, params=(user_id,))
        
        # Initialize the existing timeline as "None" for the first user
        existing_timeline = "None"
        timeline_entries = []

        # Process all the user's interviews in order
        for _, interview_row in user_interviews_df.iterrows():
            interview_text = interview_row["transcript"]
            updated_timeline = generate_user_profile(interview_text, existing_timeline)
            
            # Append to timeline entries
            timeline_entries.append(updated_timeline)
            
            # Update the existing timeline with the new entry
            existing_timeline = "\n".join(timeline_entries)

        # Step 4: Store the updated profile in Redis (optional)
        redis_client.set(f"user_timeline:{user_id}", existing_timeline)

    return "New interviews processed and Redis cache updated."
