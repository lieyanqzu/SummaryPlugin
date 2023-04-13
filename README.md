# 网页摘要-QChatGPT插件

这是一个[QChatGPT项目](https://github.com/RockChinQ/QChatGPT)的插件

通过命令在QQ对话框输入`摘要 <url>`，通过LangChain的链式摘要功能对网页内容进行摘要

如果网址为哔哩哔哩的视频页面，会使用LangChain的`BiliBiliLoader`对视频的字幕进行摘要

注意：由于我只开了ChatGPT Plus以及摘要消耗token量巨大，所以目前仅支持`revLibs`插件的逆向方式

本插件只是尝试使用langchain的链式摘要功能，以及在插件中进行多轮对话实现LLM应用的实验插件

欢迎各位大佬来一起学习交流

## 使用方式

1. 安装requirements.txt中的依赖
1. 部署[QChatGPT项目](https://github.com/RockChinQ/QChatGPT)，完成后使用管理员账号私聊机器人号发送`!plugin get https://github.com/lieyanqzu/SummaryPlugin`安装此插件
2. 前往QChatGPT插件的所在目录，修改插件顺序，让这个插件优先于其他插件
3. 修改template.py文件中的提示语模板（可选）
4. 重启主程序

此时即可向机器人发送`摘要 <url>`对网页进行内容摘要
