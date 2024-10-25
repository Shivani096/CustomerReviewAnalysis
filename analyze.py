import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import numpy as np
import matplotlib.pyplot as plt

class Analyze:
    positive = []
    negative = []
    
    def total_data(self):
        data = pd.read_excel("output.xlsx")
        return data

    def analysis(self, data):
        sen = TextBlob(data, analyzer=NaiveBayesAnalyzer())
        classificationSen = sen.sentiment.classification
        positiveSen = round(sen.sentiment.p_pos, 2) * 100
        negativeSen = round(sen.sentiment.p_neg, 2) * 100
        self.positive.append(positiveSen)
        self.negative.append(negativeSen)
        str = f"""Statement : {classificationSen}\nPositivity : {positiveSen}\nNegativity : {negativeSen}\n\n"""
        return str
    
    def get_pos_neg(self):
        self.pos = round(sum(self.positive)/len(self.positive), 2)
        self.neg = round(sum(self.negative)/len(self.negative), 2)
        return (self.pos, self.neg)

    def create_chart(self, pos, neg):
        y = np.array([pos, neg])
        x = ["Positive", "Negative"]

        myExplodes = [0.1, 0]

        plt.pie(y, labels=x, explode=myExplodes, autopct='%1.1f%%')
        plt.legend(title="Reviews in percentage : ", loc="upper left", bbox_to_anchor=(0.8,0.8))
        plt.savefig('mypng.png')
        return