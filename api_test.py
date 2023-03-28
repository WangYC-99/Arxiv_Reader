from model import *

# api = OpenAI()
# abs = '\nLogical reasoning is central to human cognition and intelligence. Past\nresearch of logical reasoning within AI uses formal language as knowledge\nrepresentation~(and symbolic reasoners). However, reasoning with formal\nlanguage has proved challenging~(e.g., brittleness and knowledge-acquisition\nbottleneck). This paper provides a comprehensive overview on a new paradigm of\nlogical reasoning, which uses natural language as knowledge representation~(and\npretrained language models as reasoners), including philosophical definition\nand categorization of logical reasoning, advantages of the new paradigm,\nbenchmarks and methods, challenges of the new paradigm, desirable tasks &amp;\nmethods in the future, and relation to related NLP fields. This new paradigm is\npromising since it not only alleviates many challenges of formal representation\nbut also has advantages over end-to-end neural methods.'
# messages = [{'role' : 'system', 'content' : '将一下内容翻译成中文：\n'}, {'role' : 'user', 'content' : abs}]
# result = api.generate_response_chatgpt(messages=messages)
# print(result)

# api = Baidu()
# src = 'Apple'
# result = api.translate(src)
# print(result)
api = BaiDuFanyi()
result = api.BdTrans('\nLogical reasoning is central to human cognition and intelligence. Past research of logical reasoning within AI uses formal language as knowledge representation~(and symbolic reasoners). However, reasoning with formal language has proved challenging~(e.g., brittleness and knowledge-acquisition bottleneck). This paper provides a comprehensive overview on a new paradigm of logical reasoning, which uses natural language as knowledge representation~(and pretrained language models as reasoners), including philosophical definition and categorization of logical reasoning, advantages of the new paradi')
print(result)