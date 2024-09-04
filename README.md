# Flask API Chat


该项目是一个基于Flask框架构建的聊天界面，通过MoonshotAI API与AI进行对话。用户可以通过网页界面发送消息，AI将返回响应。

## 项目功能
- 提供一个简单的聊天界面，允许用户输入文本并接收AI回复。
- 基于Flask框架构建，使用MoonshotAI API实现对话功能。
- 界面支持Markdown语法解析和代码高亮显示。


其中 $MOONSHOT_API_KEY 需要替换为您在平台上创建的 API Key。

*需要保证 Python 版本至少为 3.7.1，OpenAI SDK 版本不低于 1.0.0*
```
pip install --upgrade 'openai>=1.0'
```
我们可以这样简单检验下自己库的版本：
```
python -c 'import openai; print("version =",openai.__version__)'
# 输出可能是 version = 1.10.0，表示当前 python 实际使用了 openai 的 v1.10.0 的库
```

---


如有问题，请参阅[MoonshotAI API文档](https://platform.moonshot.cn/docs/intro#%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B)。
