import os

from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost

import requests
from langchain.llms.base import LLM
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders.bilibili import BiliBiliLoader

from plugins.SummaryPlugin.template import MAP_PROMPT, COMBINE_PROMPT


class QChatGPT(LLM):
    '''
    langchain LLM包裹模型
    '''

    plugin: Plugin
    kwargs: dict

    @property
    def _llm_type(self) -> str:
        return "QChatGPT"
    
    def _call(self, prompt: str, stop = None) -> str:
        self.kwargs['text_message'] = prompt
        reply = self.plugin.process_message(self.kwargs)
        return reply


# 注册插件
@register(name="Summary", description="网页摘要", version="0.1", author="lieyanqzu")
class SummaryPlugin(Plugin):

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        try:
            import plugins.revLibs.pkg.process.procmsg as procmsg
            self.process_message = lambda kwargs: procmsg.process_message(
                session_name=kwargs['launcher_type']+"_"+str(kwargs['launcher_id']), 
                prompt=kwargs['text_message'], **kwargs)
        except:
            self.process_message = lambda kwargs: "目前仅支持revLibs"
            # 没有token测试，也许是这样写吧
            # mgr = pkg.utils.context.get_qqbot_manager()
            # config = pkg.utils.context.get_config()
            # self.process_message = lambda kwargs: (pkg.qqbot.message.process_normal_message(
            #     kwargs['text_message'], mgr, config, kwargs['launcher_type'], kwargs['launcher_id'], kwargs['sender_id']))[0]

    # 当收到个人消息和群聊消息时触发
    @on(PersonNormalMessageReceived)
    @on(GroupNormalMessageReceived)
    def normal_message_received(self, event: EventContext, **kwargs):
        msg = kwargs['text_message']
        # 如果消息为摘要 <url>则触发
        if msg.startswith("摘要 "):
            msg_seg = msg.split(' ')
            if len(msg_seg) < 2:
                reply = '格式：摘要 <url>'
            else:
                url = msg_seg[1]
                docs = None
                tmp_file_path = './tmp.html'
                # B站视频使用BiliBiliLoader读取
                if "www.bilibili.com/video/" in url:
                    loader = BiliBiliLoader([url])
                    docs = loader.load()
                # 不是B站视频或者视频没有字幕文件则下载网页读取
                if docs is None or docs[0].page_content == '':
                    # UnstructuredURLLoader不能正确处理编码，所以先用requests
                    req = requests.get(url)
                    req.encoding = 'utf-8'
                    html = req.text
                    with open(tmp_file_path, 'w', encoding='utf-8') as tmp_file:
                        tmp_file.write(html)
                        loader = UnstructuredHTMLLoader(tmp_file.name)
                    docs = loader.load()

                # 对文本进行分段，防止丢进gpt超过最大长度
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                split_docs = text_splitter.split_documents(docs)

                llm = QChatGPT(plugin=self, kwargs=kwargs)
                chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True, map_prompt=MAP_PROMPT, combine_prompt=COMBINE_PROMPT)
                reply = chain.run(input_documents=split_docs)

                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
                
            # 输出调试信息
            logging.debug(reply)

            # 回复消息
            event.add_return("reply", [reply])

            # 阻止该事件默认行为（向接口获取回复）
            event.prevent_default()
            event.prevent_postorder()

    # 插件卸载时触发
    def __del__(self):
        pass
