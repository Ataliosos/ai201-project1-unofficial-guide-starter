# The Unofficial Guide — Project 1

## Domain

My system covers unofficial student knowledge about CUNY City Tech professors. It allows students to search through professor reviews to learn about teaching style, grading practices, exam difficulty, homework workload, attendance expectations, extra credit opportunities, and how helpful professors are.

This knowledge is valuable because official college resources only provide course descriptions and faculty names. They do not reflect students' actual classroom experiences. Students often rely on websites like Rate My Professors or advice from classmates to make informed decisions about course registration.

---

## Document Sources

| #  | Source                       | Type      | URL or File Path             |
| -- | ---------------------------- | --------- | ---------------------------- |
| 1  | Boris Gelman Reviews         | Text File | boris_gelman.txt             |
| 2  | Roman Kezerashvili Reviews   | Text File | roman_kezerashvili.txt       |
| 3  | Vaneet Singh Reviews         | Text File | vaneet_singh.txt             |
| 4  | Jeffery Kroll Reviews        | Text File | jeffery_kroll.txt            |
| 5  | Suela Aalsberg Reviews       | Text File | suela_aalsberg.txt           |
| 6  | Farrukh Zia Reviews          | Text File | farrukh_zia.txt              |
| 7  | Sarah Schmerler Reviews      | Text File | sarah_schmerler.txt          |
| 8  | Jared Day Reviews            | Text File | jared_day.txt                |
| 9  | Ahmed Hassebo Reviews        | Text File | ahmed_hassebo.txt            |
| 10 | Additional Professor Reviews | Text File | Other collected review files |

---

## Chunking Strategy

**Chunk size:** One complete review per chunk.

**Overlap:** No overlap.

**Why these choices fit your documents:** The documents consisted of short professor reviews. Treating each review as a single chunk preserved complete opinions and avoided splitting important information across chunk boundaries. This made each chunk meaningful and retrievable on its own.

**Final chunk count:** 162 chunks.

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 using Sentence Transformers.

**Production tradeoff reflection:** This model was chosen because it runs locally, requires no API key, and is efficient for small projects. For a production system, I would consider larger embedding models with better multilingual capabilities and higher retrieval accuracy, although they would increase computational cost and latency.

---

## Grounded Generation

**System prompt grounding instruction:**

The system prompt instructed the language model to answer only using the retrieved document context:

"Use ONLY the context below. Do not use outside knowledge. If the context does not contain enough information, say: 'I don't have enough information in the documents to answer that.'"

**How source attribution is surfaced in the response:**

The retrieved source filenames were collected programmatically and returned alongside the generated answer so users could identify which documents supported the response.

---

## Evaluation Report

| # | Question                                                        | Expected Answer                             | System Response (Summarized)                                                            | Retrieval Quality  | Response Accuracy |
| - | --------------------------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------ | ----------------- |
| 1 | What do students say about Boris Gelman's grading?              | Lenient and fair grader.                    | Students described him as an easy grader and generous with grading.                     | Relevant           | Accurate          |
| 2 | What do students say about Roman Kezerashvili's difficulty?     | Difficult, unclear, challenging.            | Students described him as difficult and hard to understand.                             | Relevant           | Accurate          |
| 3 | What do students say about Jeffery Kroll's math teaching?       | Clear explanations and helpful instruction. | Students reported learning concepts clearly and succeeding through his explanations.    | Relevant           | Accurate          |
| 4 | What do students say about Vaneet Singh's grading and homework? | Easy grading and manageable work.           | The system stated there was insufficient information despite relevant reviews existing. | Partially Relevant | Inaccurate        |
| 5 | What is the first match of the 2026 FIFA World Cup?             | The system should refuse to answer.         | The system correctly stated it lacked enough information in the documents.              | Relevant           | Accurate          |

Overall, the system answered 4 out of 5 evaluation questions accurately, resulting in an 80% accuracy rate.

---

## Failure Case Analysis

**Question that failed:** What do students say about Vaneet Singh's grading and homework?

**What the system returned:** The system responded that it did not have enough information to answer the question.

**Root cause:** The retrieval stage returned unrelated reviews from other professors because the embedding model matched general educational terms such as "grading" and "homework" across multiple sources.

**What you would change to fix it:** I would implement metadata filtering by professor name or combine semantic retrieval with keyword search to improve retrieval precision.

---

## Spec Reflection

**One way the spec helped during implementation:**

The planning document forced me to think through my chunking strategy, retrieval design, evaluation plan, and architecture before writing code. This made debugging easier because each component had a clearly defined purpose.

**One way implementation diverged from the spec, and why:**

During testing, retrieval occasionally returned unrelated professor reviews. Instead of assuming the system worked perfectly, I adjusted my evaluation and documented these limitations. This divergence highlighted the importance of iterative testing and honest reporting.

---

## AI Usage

### Instance 1

* What I gave the AI: My planning document, chunking strategy, and document descriptions.
* What it produced: An ingestion and chunking pipeline implementation.
* What I changed or overrode: I modified the implementation to preserve metadata including source filenames, review numbers, and chunk positions.

### Instance 2

* What I gave the AI: Retrieval requirements, generation requirements, and Gradio interface specifications.
* What it produced: ChromaDB retrieval functions, Groq generation code, and a Gradio interface.
* What I changed or overrode: I refined retrieval settings, improved grounding instructions, and documented retrieval failures instead of accepting the original implementation without testing.
