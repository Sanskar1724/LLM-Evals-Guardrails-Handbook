"""
Chapter 5 - Evaluating RAG (retrieval-augmented generation).

Run:  python ch05_rag_metrics.py

A RAG app has two parts:
  retriever -> finds text chunks for the question
  generator -> writes the answer using those chunks

Part 1: retrieval metrics (precision@k, recall@k, MRR).
Part 2: faithfulness - is every claim in the answer supported by the chunks?
Part 3: answer relevance - does the answer talk about the question?

Real tools (for example Ragas) use an LLM to split the answer into claims
and to check each claim. Here we use simple word rules so it runs anywhere.
The rules are rough. They show the idea, not the best method.

No key needed. Standard library only.
"""

import re

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "to", "of", "in", "on",
    "at", "for", "and", "or", "it", "its", "this", "that", "with", "as", "by",
    "from", "you", "your", "can", "will", "do", "does", "what", "how", "when",
    "where", "which", "who", "i", "we", "our", "my", "has", "have", "after",
}


def content_words(text):
    """Lower-case words without very common words."""
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP_WORDS}


# ---------- Part 1: retrieval ----------

def precision_at_k(retrieved_ids, relevant_ids, k):
    top = retrieved_ids[:k]
    return sum(1 for doc in top if doc in relevant_ids) / k


def recall_at_k(retrieved_ids, relevant_ids, k):
    top = retrieved_ids[:k]
    return sum(1 for doc in top if doc in relevant_ids) / len(relevant_ids)


def reciprocal_rank(retrieved_ids, relevant_ids):
    """1 / position of the first relevant chunk. First place = 1.0, second = 0.5 ..."""
    for position, doc in enumerate(retrieved_ids, start=1):
        if doc in relevant_ids:
            return 1 / position
    return 0.0


# ---------- Part 2: faithfulness ----------

def split_into_claims(answer):
    """Very simple: one sentence = one claim."""
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", answer) if s.strip()]


def claim_is_supported(claim, chunks, threshold=0.7):
    """
    A claim counts as supported if:
      * all its numbers appear in one chunk, and
      * at least `threshold` of its content words appear in that chunk.
    """
    claim_words = content_words(claim)
    claim_numbers = set(re.findall(r"\d+", claim))
    if not claim_words:
        return True
    for chunk in chunks:
        chunk_words = content_words(chunk)
        chunk_numbers = set(re.findall(r"\d+", chunk))
        share = len(claim_words & chunk_words) / len(claim_words)
        if share >= threshold and claim_numbers <= chunk_numbers:
            return True
    return False


def faithfulness(answer, chunks):
    """Supported claims / all claims. 1.0 = nothing was made up."""
    claims = split_into_claims(answer)
    results = [(claim, claim_is_supported(claim, chunks)) for claim in claims]
    score = sum(ok for _, ok in results) / max(1, len(results))
    return score, results


# ---------- Part 3: answer relevance ----------

def answer_relevance(question, answer):
    """Share of the question's content words that the answer also uses. Very rough."""
    q_words = content_words(question)
    a_words = content_words(answer)
    return len(q_words & a_words) / max(1, len(q_words))


def main():
    print("PART 1 - retrieval")
    retrieved = ["doc7", "doc2", "doc9", "doc4", "doc1"]   # what the retriever returned, best first
    relevant = {"doc2", "doc4", "doc8"}                    # what a human marked as useful
    print("  retrieved:", retrieved)
    print("  relevant :", sorted(relevant))
    print(f"  precision@3 = {precision_at_k(retrieved, relevant, 3):.2f}")
    print(f"  recall@3    = {recall_at_k(retrieved, relevant, 3):.2f}")
    print(f"  recall@5    = {recall_at_k(retrieved, relevant, 5):.2f}")
    print(f"  reciprocal rank = {reciprocal_rank(retrieved, relevant):.2f}")

    print()
    print("PART 2 - faithfulness")
    chunks = [
        "Refunds are sent to the original payment method within 5 working days.",
        "Orders above 500 rupees get free delivery. Other orders pay 40 rupees.",
    ]
    question = "How long does a refund take and where is the refund sent?"
    good_answer = "Refunds are sent to the original payment method. Refunds take 5 working days."
    bad_answer = "Refunds are sent to the original payment method. Refunds take 2 working days. You also get a 100 rupees gift card."

    for name, answer in [("good answer", good_answer), ("bad answer", bad_answer)]:
        score, details = faithfulness(answer, chunks)
        print(f"  {name}: faithfulness = {score:.2f}")
        for claim, ok in details:
            print(f"     [{'supported' if ok else 'NOT supported'}] {claim}")

    print()
    print("PART 3 - answer relevance")
    off_topic = "Our company was started in 2015 and we love our customers."
    print(f"  good answer : {answer_relevance(question, good_answer):.2f}")
    print(f"  off-topic   : {answer_relevance(question, off_topic):.2f}")
    print()
    print("Note: an answer can be faithful but not relevant, or relevant but not faithful.")
    print("That is why RAG evals measure both.")


if __name__ == "__main__":
    main()
