from url_summarize import URLSummarize

urlsum = URLSummarize("http://www.foxnews.com/politics/2017/01/02/hill-democrats-outline-counter-attack-for-obamacare-repeal-prep-for-presidents-visit.html")
summary = urlsum.summarize_article(5,2)

print(summary)