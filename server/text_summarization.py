from transformers import pipeline
summarizer = pipeline(
    "summarization", model="facebook/bart-large-cnn")


def get_summarized_text(text, max_length=100):
    result = summarizer(text, max_length=max_length, min_length=min(
        max_length, len(text)), do_sample=False)
    return "" if len(result) == 0 else result[0]['summary_text']
