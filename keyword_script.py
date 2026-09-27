import os
import json
import time
from groq import Groq
from dotenv import load_dotenv



# 1. LOAD GROQ API KEY


load_dotenv()

api_key = ""

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)



# 2. FILE SETTINGS


INPUT_FILE = "Session_1_no_timestamps.txt"
KEYWORDS_FILE = "keywords_output.json"
BLOG_FILE = "final_blog.txt"

WORDS_PER_CHUNK = 500

# You can change the model depending on the Groq models
# currently available to your account.
MODEL = "openai/gpt-oss-120b"


# 3. READ TRANSCRIPT


def read_transcript(filename):

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    return text



# 4. SPLIT TRANSCRIPT INTO 500-WORD CHUNKS


def split_into_chunks(text, words_per_chunk=500):

    words = text.split()

    chunks = []

    for i in range(0, len(words), words_per_chunk):

        chunk = " ".join(words[i:i + words_per_chunk])

        chunks.append(chunk)

    return chunks



# 5. PROMPT FOR EDUCATIONAL KEYWORD EXTRACTION


def create_keyword_prompt(chunk, chunk_number):

    prompt = f"""
You are an expert educational SEO keyword researcher.

I am creating an educational blog from a long educational
video transcript.

Analyze the following transcript section carefully.

Your task is to identify the most important and useful
educational keywords and keyphrases from this section.

Focus on:

1. Main educational topics
2. Important concepts
3. Technical terms
4. Subject-specific terminology
5. Important entities
6. Search-friendly educational phrases
7. Long-tail educational keywords
8. Concepts that can become blog headings
9. Terms that students may search for
10. Terms that help explain the subject clearly

DO NOT select:
- Random words
- Filler words
- Greetings
- Repeated generic words
- Unimportant conversational phrases
- Keywords unrelated to the educational topic

Prefer meaningful phrases such as:

"machine learning algorithms"
"supervised learning"
"data preprocessing techniques"

instead of generic words such as:

"good"
"video"
"important"
"learn"

IMPORTANT:
Only extract keywords that are supported by the transcript.
Do not invent concepts that are not present in the transcript.

Return ONLY valid JSON in the following format:

{{
    "chunk_number": {chunk_number},
    "keywords": [
        {{
            "keyword": "keyword phrase",
            "importance": "high",
            "reason": "short explanation"
        }}
    ]
}}

Return approximately 10-20 of the most relevant keywords.

Transcript section:

--- START TRANSCRIPT ---

{chunk}

--- END TRANSCRIPT ---
"""

    return prompt



# 6. SEND EACH 500-WORD CHUNK TO GROQ


def extract_keywords(chunk, chunk_number):

    prompt = create_keyword_prompt(chunk, chunk_number)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert educational SEO researcher "
                    "and content strategist."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    result = response.choices[0].message.content

    return result



# 7. PROCESS ALL CHUNKS


def process_transcript(chunks):

    all_keywords = []

    total_chunks = len(chunks)

    print(f"\nTotal chunks: {total_chunks}\n")

    for index, chunk in enumerate(chunks, start=1):

        print(
            f"Processing chunk {index}/{total_chunks}..."
        )

        try:

            result = extract_keywords(
                chunk,
                index
            )

            print("LLM response received.")

            # Try converting LLM response to JSON
            try:

                data = json.loads(result)

                all_keywords.append(data)

            except json.JSONDecodeError:

                print(
                    f"Warning: Chunk {index} returned invalid JSON."
                )

                all_keywords.append(
                    {
                        "chunk_number": index,
                        "raw_response": result
                    }
                )

        except Exception as e:

            print(
                f"Error processing chunk {index}: {e}"
            )

        # Small delay to avoid hitting rate limits
        time.sleep(1)

    return all_keywords



# 8. SAVE KEYWORDS


def save_keywords(data, filename):

    with open(filename, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nKeywords saved to: {filename}"
    )



# 9. MAIN PROGRAM


def main():

    print("Reading transcript...")

    transcript = read_transcript(INPUT_FILE)

    print(
        f"Transcript contains approximately "
        f"{len(transcript.split())} words."
    )

    print("\nSplitting transcript...")

    chunks = split_into_chunks(
        transcript,
        WORDS_PER_CHUNK
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    keywords = process_transcript(chunks)

    save_keywords(
        keywords,
        KEYWORDS_FILE
    )

    print("\nKeyword extraction completed.")


if __name__ == "__main__":
    main()