 
import re
from collections import defaultdict
class TransactionCategorizer:
    def __init__(self):
        self.rules ={
            "Food" : ["grocery", "food", "restaurant", "pizza", "snack", "coffee", "burger"],
            "Transport" : ["snap", "snapp", "taxi", "uber", "bus", "train", "fuel", "parking", "plane", "airplane", "air-plane"],
            "Income" : ["salary", "bonus", "income", "paycheck", "payment"],
            "Health" : ["medicine", "doctor", "hospital", "pharmacy", "clinic"],
            "Shopping" : ["clothes", "shoe", "shopping", "mall", "gift"],
            "Utilities": ["electric", "water", "internet", "wifi", "utility", "bill", "gas-bill", "gas"],
            "Entertainment" : ["movie", "cinema", "game", "netflix", "spotify"]
        }
        self.default_category = "Other"
    def preprocess(self, text:str):
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        return words
    def categorize(self, description: str) -> str:
        words = self.preprocess(description)
        votes = defaultdict(int)
        for word in words :
            for category, keywords in self.rules.items():
                if word in keywords:
                    votes[category]+=1
        if not votes:
            return self.default_category
        return max(votes, key=votes.get)
categorizer = TransactionCategorizer()
def auto_category(description : str):
    return categorizer.categorize(description)