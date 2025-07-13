# Google Generative AI 库安装指南

由于网络连接问题，我们需要手动安装 `google-generativeai` 库。以下是几种解决方案：

## 方法1：离线安装（推荐）

### 步骤1：下载安装包
1. 访问 [PyPI google-generativeai页面](https://pypi.org/project/google-generativeai/#files)
2. 下载最新版本的 `.whl` 文件（选择适合Windows的版本）
3. 将文件保存到项目目录

### 步骤2：离线安装
```bash
# 激活虚拟环境
deepseek_agent_env\Scripts\activate

# 安装下载的whl文件
pip install google_generativeai-0.8.3-py3-none-any.whl
```

## 方法2：修复网络配置

### 检查代理设置
```bash
# 检查pip配置
pip config list

# 如果有代理设置，可以临时取消
pip install --proxy="" google-generativeai
```

### 使用不同的镜像源
```bash
# 使用阿里云镜像
pip install -i https://mirrors.aliyun.com/pypi/simple/ google-generativeai

# 使用豆瓣镜像
pip install -i https://pypi.douban.com/simple/ google-generativeai
```

## 方法3：使用系统Python安装

如果虚拟环境有问题，可以先在系统Python中安装：

```bash
# 使用系统Python安装
python -m pip install google-generativeai

# 然后复制到虚拟环境
```

## 方法4：手动下载依赖

如果以上方法都不行，可以手动下载所有依赖：

1. `google-generativeai`
2. `google-ai-generativelanguage`
3. `google-auth`
4. `google-api-core`
5. `protobuf`
6. `requests`

## 验证安装

安装完成后，运行以下命令验证：

```bash
python -c "import google.generativeai as genai; print('安装成功！')"
```

## 如果仍然有问题

1. 检查防火墙设置
2. 检查公司网络代理
3. 尝试使用手机热点
4. 联系网络管理员

## 临时解决方案

如果暂时无法安装，我已经创建了一个模拟版本的Gemini客户端，可以先测试项目结构：

```python
# 在gemini_client.py中临时使用模拟版本
class GeminiLLM(LLM):
    def _call(self, prompt, **kwargs):
        return "这是模拟的Gemini响应，请安装google-generativeai库后使用真实API"
```
