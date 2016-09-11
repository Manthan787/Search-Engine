INDEX = '1512_great_mordenist_artist'
TYPE = 'document'
RESULT_SIZE = 200
RESULTS_PATH = '/Users/admin/Documents/CS6200/HW5/Evaluator/Results'
QRELS_PATH = '/Users/admin/Documents/CS6200/HW5/Evaluator/qrels.1512.txt'
NDCG_QRELS_PATH = '/Users/admin/Documents/CS6200/HW5/Evaluator/qrels.txt'
SEARCH_BODY = """
{{
    "query": {{
        "query_string": {{
          "default_field": "TEXT",
          "query": "{}"
        }}
    }}
}}
"""


# QREL File INDEX Aliases
QID = 0
ASSESSORID = 1
DOCID = 2
GRADE = 3

# TREC Format Result file INDEX Aliases
RESULT_QID = 0
RESULT_DOCID = 2
RESULT_RANK = 3
RESULT_SCORE = 4

# k's for precision@k, recall@k and F1@k
k = [5, 10, 20, 50, 100]


# Path for all the Plots to store
PLOT_PATH = '/Users/admin/Documents/CS6200/HW5/Evaluator/Plots'

# Summary
OUTPUT =  """
    queryID (num)       : {ID}
    Total Relevant      : {R}
    Rel_ret             : {rel_ret}
    R-Precision         : {rp}
    Average Precision   : {avg_prec}
    ndcg                : {ndcg}

    Precision:
    At    5 docs:    {prec_5}
    At   10 docs:    {prec_10}
    At   20 docs:    {prec_20}
    At   50 docs:    {prec_50}
    At  100 docs:    {prec_100}

    Recall:
    At    5 docs:    {rec_5}
    At   10 docs:    {rec_10}
    At   20 docs:    {rec_20}
    At   50 docs:    {rec_50}
    At  100 docs:    {rec_100}

    F-Measure:
    At    5 docs:    {f1_5}
    At   10 docs:    {f1_10}
    At   20 docs:    {f1_20}
    At   50 docs:    {f1_50}
    At  100 docs:    {f1_100}

"""
