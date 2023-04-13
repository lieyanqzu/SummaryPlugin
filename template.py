from langchain.prompts import PromptTemplate

# 分块摘要提示语模板
map_prompt_template = """用中文写一篇简洁的摘要，概括以下内容：


"{text}"


简要摘要："""
MAP_PROMPT = PromptTemplate(template=map_prompt_template, input_variables=["text"])

# 分块合并摘要提示语模板
combine_prompt_template = """用中文写一篇简洁的摘要，概括以下内容，以下内容为同一内容的不同部分的摘要，不要按分段而应该作为一个整体进行摘要：


"{text}"


简要摘要："""
COMBINE_PROMPT = PromptTemplate(template=combine_prompt_template, input_variables=["text"])
