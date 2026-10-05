# youtube-blog-generator
AI project that converts YouTube transcripts into SEO-optimized blog content.
# Transcript to Educational Content using Groq LLM

An LLM-powered pipeline that converts a long educational transcript into **important SEO keywords, a keyword hierarchy, and a short educational video script** using the Groq API.

## Project Workflow

```text
Educational Transcript
        ↓
Split into 500-word chunks
        ↓
Groq LLM
        ↓
Extract educational keywords
        ↓
keywords_output.json
        ↓
Create keyword hierarchy
        ↓
keyword_hierarchy.md
        ↓
Generate 180–220 word video script
        ↓
final_blog.md
```

## Features

* Splits a long transcript into **500-word chunks**
* Uses **Groq LLM** to extract important educational keywords
* Identifies:

  * Main educational topics
  * Technical terms
  * Important concepts
  * Long-tail keywords
  * Student-focused search terms
* Removes duplicate keywords
* Creates a **parent-child keyword hierarchy**
* Generates a **180–220 word educational video script**
* Ensures generated content is based only on the provided transcript
* Saves results in reusable JSON and Markdown files

## Technologies Used

* Python
* Groq API
* `groq`
* `python-dotenv`
* JSON
* Regular Expressions

## Project Structure

```text
project/
│
├── Session_1_no_timestamps.txt
├── keyword_extractor.py
├── keyword_hierarchy.py
├── keywords_output.json
├── keyword_hierarchy.md
├── final_blog.md
├── .env
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### 2. Install dependencies

```bash
pip install groq python-dotenv
```

### 3. Add your Groq API key

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key
```

**Do not commit your `.env` file or API key to GitHub.**

Add this to `.gitignore`:

```text
.env
__pycache__/
```

## Input

Place your cleaned transcript in the project directory:

```text
Session_1_no_timestamps.txt
```

The transcript should contain the educational content without timestamps.

## Step 1 — Keyword Extraction

The first script:

```text
keyword_extractor.py
```

splits the transcript into **500-word chunks** and sends each chunk to the Groq LLM.

The LLM extracts relevant educational keywords and saves them in:

```text
keywords_output.json
```

Example:

```json
{
    "chunk_number": 1,
    "keywords": [
        {
            "keyword": "machine learning algorithms",
            "importance": "high",
            "reason": "Important concept discussed in the transcript."
        }
    ]
}
```

## Step 2 — Keyword Hierarchy & Script Generation

The second script processes the extracted keywords and:

1. Removes duplicate keywords
2. Creates a parent-child keyword hierarchy
3. Uses the transcript to validate keyword relationships
4. Generates a **180–220 word educational video script**

Outputs:

```text
keyword_hierarchy.md
final_blog.md
```

## Run the Project

Run the keyword extraction script first:

```bash
python keyword_extractor.py
```

Then run the hierarchy and script generation script:

```bash
python keyword_hierarchy.py
```

## Output

| File                   | Purpose                                       |
| ---------------------- | --------------------------------------------- |
| `keywords_output.json` | Keywords extracted from each transcript chunk |
| `keyword_hierarchy.md` | Parent-child hierarchy of important keywords  |
| `final_blog.md`        | Generated educational video script            |

## Model

The project uses:

```text
openai/gpt-oss-120b
```

through the Groq API.

## Important Design Principle

The prompts are designed to keep the generated content **grounded in the source transcript**.

The model is instructed not to:

* Invent facts
* Add unsupported concepts
* Add unrelated keywords
* Keyword-stuff the content
* Generate information that is not present in the source

This helps maintain factual consistency between the transcript and the generated content.

## Future Improvements

* Automatic SEO title and meta description generation
* Keyword ranking based on relevance
* Blog outline generation
* Full-length blog generation
* Web interface using Streamlit
* YouTube transcript API integration
* Automatic publishing workflow
* Keyword frequency and semantic similarity analysis

## Author

**Janhvi Jain**

Built as an LLM-based educational content generation and SEO keyword extraction project.
