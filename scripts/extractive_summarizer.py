from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import nltk

nltk.download('punkt')
nltk.download('stopwords')

def extractive_summarization(text: str, compression_ratio: int) -> str:
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    all_words = word_tokenize(text.lower())
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in all_words if word.isalnum() and word not in stop_words]
    
    # Calculate word frequencies
    freq = FreqDist(words)
    
    # Score sentences based on word frequencies
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        sentence_words = word_tokenize(sentence.lower())
        for word in sentence_words:
            if word in freq:
                if i in sentence_scores:
                    sentence_scores[i] += freq[word]
                else:
                    sentence_scores[i] = freq[word]
    
    # Calculate target word count based on compression ratio
    target_word_count = int(len(all_words) * compression_ratio / 100)
    
    # Select top sentences until we reach or exceed the target word count
    top_sentences = []
    current_word_count = 0
    for i in sorted(sentence_scores, key=sentence_scores.get, reverse=True):
        sentence_word_count = len(word_tokenize(sentences[i]))
        if current_word_count + sentence_word_count <= target_word_count:
            top_sentences.append(i)
            current_word_count += sentence_word_count
        else:
            break
    
    # Construct the summary as a bulleted list
    summary = "\n".join([f"• {sentences[i].strip()}" for i in sorted(top_sentences)])
    
    return summary