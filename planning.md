# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

My domain is the unofficial guide to CUNY City Tech professors. This system will help students search student-generated reviews about professors, including teaching style, grading, exam difficulty, homework, attendance, extra credit, and how helpful the professor is.

This knowledge is valuable because official City Tech pages only show basic course and professor information. They do not show what students actually experience in class, so students usually rely on Rate My Professors, classmates, and unofficial advice.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors | Student reviews for Vaneet Singh | documents/vaneet_singh.txt |
| 2 | Rate My Professors | Student reviews for Jared Day | documents/jared_day.txt |
| 3 | Rate My Professors | Student reviews for Farrukh Zia | documents/farrukh_zia.txt |
| 4 | Rate My Professors | Student reviews for Boris Gelman | documents/boris_gelman.txt |
| 5 | Rate My Professors | Student reviews for Roman Kezerashvili | documents roman_kezerashvili.txt |
| 6 | Rate My Professors | Student reviews for Mohammed Islam | documents/mohammed_islam.txt |
| 7 | Rate My Professors | Student reviews for Ahmed Hassebo | documents/ahmed_hassebo.txt |
| 8 | Rate My Professors | Student reviews for Jeffery Kroll | documents/jeffery_kroll.txt |
| 9 | Rate My Professors | Student reviews for Suela Aalsberg | documents/suela_aalsberg.txt |
| 10 | Rate My Professors | Student reviews for Sarah Schmerler | documents/sarah_schmerler.txt |

## Chunking Strategy

**Chunk size:** One review per chunk. If a review is longer than about 500 characters, split it into smaller chunks.

**Overlap:** 100 characters for long reviews that need to be split.

**Reasoning:** My documents are mostly short professor reviews. Each review already includes the course, date, quality, difficulty, and student opinion, so keeping one review together makes the chunk easier to understand. If chunks are too small, the system may retrieve only a rating without the explanation. If chunks are too large, reviews about different professors or different classes may get mixed together.

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` using `sentence-transformers`.

**Top-k:** 5 chunks per query.

**Production tradeoff reflection:** For a real production system, I would compare embedding models based on accuracy, speed, cost, context length, multilingual support, and whether the model runs locally or uses an API. A local model is free and private, but a larger API model may understand harder or more detailed student questions better.

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Professor Vaneet Singh’s grading and difficulty? | Students mostly say Professor Singh is lenient or fair, his work is straightforward, and the class is low difficulty if students follow instructions and attend. |
| 2 | Which professor has reviews mentioning extra credit and clear explanations in math? | Jeffery Kroll has many reviews saying he explains math clearly, gives extra credit, and helps students understand. |
| 3 | What do students say about Professor Roman Kezerashvili’s difficulty? | Reviews are mixed, but many students describe him as difficult, lecture-heavy, and hard to understand, while some say he is knowledgeable and good if students keep up. |
| 4 | Which professor is described as caring and flexible in Economics? | Suela Aalsberg is described as caring, flexible, clear, and helpful, with easy or manageable assignments and exams. |
| 5 | What do students say about Professor Mohammed Islam’s teaching style? | Reviews are mixed. Some students say he is clear, helpful, and good for robotics or EMT classes, while others say he can be unorganized, spends time on his phone, or makes students teach themselves. |

## Anticipated Challenges

1. Student reviews are subjective and sometimes contradict each other. A professor can have both very positive and very negative reviews, so the system needs to give balanced answers instead of only showing one side.

2. Chunking could cause problems if a review is split badly. If the rating, course, and review text are separated, the system may retrieve incomplete context.

3. Source attribution could be missed if metadata is not stored correctly. Every chunk needs the professor file name so answers can cite the source.

## Architecture

```mermaid
flowchart LR
    A[Document Ingestion: TXT files in documents folder] --> B[Chunking: split by review]
    B --> C[Embedding: all-MiniLM-L6-v2]
    C --> D[Vector Store: ChromaDB]
    D --> E[Retrieval: top 5 chunks]
    E --> F[Generation: Groq llama-3.3-70b-versatile]

AI Tool Plan

Milestone 3 — Ingestion and chunking:
I will use ChatGPT to help implement a script that loads all .txt files from the documents folder, cleans extra whitespace, and splits the text by review. I will give ChatGPT my Documents and Chunking Strategy sections. I will verify the output by printing 5 chunks and checking that each chunk is readable and includes the professor source.

Milestone 4 — Embedding and retrieval:
I will use ChatGPT to help implement embeddings with all-MiniLM-L6-v2 and store chunks in ChromaDB with metadata. I will give ChatGPT my Retrieval Approach and Architecture sections. I will verify the output by testing at least 3 evaluation questions and checking that the returned chunks match the question.

Milestone 5 — Generation and interface:
I will use ChatGPT to help write a grounded prompt and a simple interface. I will give ChatGPT my Evaluation Plan and grounding requirement. I will verify the output by asking one question that is covered by the documents and one question that is not covered. The system should cite sources for covered questions and refuse to answer unsupported questions.
