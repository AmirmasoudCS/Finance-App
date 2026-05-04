 
import re
from typing import Dict, Tuple, Optional
from collections import defaultdict
from nltk.stem import PorterStemmer
from rapidfuzz import fuzz
class TransactionCategorizer:
    def __init__(self):
        self.rules ={
            "Food" : {
                "Groceries" : {"grocery", "market"},
                "Restaurant" : {"restaurant", "pizza", "burger", "food"},
                "Coffee" : {"coffee", "cafe"}
            },
            "Transport" : {
                "Taxi" : {"snap", "snapp", "taxi", "uber"},
                "Fuel" : {"fuel", "gas"},
                "Public Transport" : {"bus", "train"},
                "Flights" : {"plane", "airplane"}
            },
            "Income" : {
                "Salary" : {"salary", "paycheck"},
                "Bonus" : {"bonus"},
                "Profit" : {"profit", "payment", "bank profit"}
            },
            "Health" : {
                "Medicine" : {"medicine", "pharmacy", "drug", "drugstore"},
                "Doctor" : {"doctor", "clinic", "hospital", "visit"}
            },
            "Shopping" : {
                "Clothes" : {"clothes", "shoe"},
                "General" : {"shopping", "mall", "gift"}
            },
            "Utilities": {
                "Bills" : {"electric", "water", "gas", "bill"},
                "Internet" : {"internet", "wifi", "network"}
            },
            "Entertainment" : {
                "Movies" : {"movie", "cinema", "theater", "netflix"},
                "Music" : {"spotify"},
                "Games" : {"game", "steam"}
            }
        }
        self.default_category = "Other"
        self.stemmer = PorterStemmer()
    def preprocess(self, text:str) -> list[str]:
        text = re.sub(r"[^\w\s]", "", text.lower())
        return text.split()
    def stem(self, words: list[str]) -> list[str]:
        return [self.stemmer.stem(w) for w in words]
    def categorize(self, description: str) -> tuple[str, Optional[str]]:
        words = self.stem(self.preprocess(description))
        category_votes : Dict[str, int] = defaultdict(int)
        subcategory_votes : Dict[Tuple[str, str], int] = defaultdict(int)
        for category, subcats in self.rules.items():
            for subcat, keywords in subcats.items():
                stemmed_keywords = {self.stemmer.stem(k) for k in keywords}
                if any(w in stemmed_keywords or fuzz.partial_ratio(w, kw) > 85 for w in words for kw in keywords):
                    category_votes[category] += 1
                    subcategory_votes[(category, subcat)] += 1
        if not category_votes:
            return self.default_category, None
        categories = list(category_votes.keys())
        best_category = max(categories, key=lambda c :category_votes[c])
        best_subcategory = None
        best_score = 0
        for (cat, subcat), score in subcategory_votes.items():
            if cat == best_category and score > best_score:
                best_score = score
                best_subcategory = subcat
        return best_category, best_subcategory
categorizer = TransactionCategorizer()
def auto_category(description : str) -> tuple[str, str | None]:
    return categorizer.categorize(description)