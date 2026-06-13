import json
import re
from rank_bm25 import BM25Okapi
from nltk.stem import PorterStemmer
import nltk

nltk.download('punkt', quiet=True)

INDEX_PATH = ".kb/index.json"

STOP_WORDS = {
    "can", "i", "how", "the", "is", "a", "my", "what", "where",
    "when", "who", "which", "do", "does", "get", "an", "in",
    "on", "at", "to", "for", "of", "and", "or", "be", "will"
}

SYNONYMS = {
    "money back": "refund",
    "return":     "refund",
    "reimburse":  "refund",
    "ship":       "shipping",
    "deliver":    "shipping",
    "delivery":   "shipping",
    "cancel":     "cancellation",
}

stemmer = PorterStemmer()

def normalize(text):
    text = re.sub(r'[^\w\s]', '', text)  # 移除標點符號
    words = text.lower().split()
    words = [w for w in words if w not in STOP_WORDS]  # 移除停用詞
    words = [stemmer.stem(w) for w in words]            # 字根還原
    return words

def expand_query(words):
    expanded = list(words)
    # 先試兩個字的組合
    for i in range(len(words) - 1):
        bigram = words[i] + " " + words[i+1]
        if bigram in SYNONYMS:
            expanded.append(stemmer.stem(SYNONYMS[bigram]))
    # 再試單字
    for w in words:
        if w in SYNONYMS:
            expanded.append(stemmer.stem(SYNONYMS[w]))
    return expanded

def load_index():
    return json.load(open(INDEX_PATH, encoding="utf-8"))


# BM25 的算法：
# score = 關鍵字稀不稀有 × 出現頻率 × 文件長度補償
def search(question, top_k=3):
    chunks = load_index()
    
    # 每個 chunk 的文字切成單字列表
    corpus = [
        (chunk["heading"] + " " + chunk["content"]).lower().split()
        for chunk in chunks
    ]
    
    # 建立 BM25 索引
    bm25 = BM25Okapi(corpus)
    
    query = normalize(question)
    query = expand_query(query)          # 同義詞擴展
    print(f"Query tokens: {query}")
        
    
    # 算每個 chunk 的分數
    scores = bm25.get_scores(query)
    
    # 排序，取前 top_k 個
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
    return [chunk for score, chunk in ranked[:top_k] if score > 0]


if __name__ == "__main__":
    questions = [
        "What is the refund policy?",           # 直接關鍵字
        "How can I get my money back?",          # 同義詞挑戰
        "Under which condition I can get my money back?",  # 口語
    ]
    for q in questions:
        print(f"\n❓ {q}")
        results = search(q)
        if results:
            for r in results:
                print(f"   📄 {r['source']}")
        else:
            print("   ❌ 找不到")



