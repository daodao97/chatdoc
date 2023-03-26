# ChatDoc

一个使用 `openai` 与文档对话的例子, 目前支持的文档类型

- `.pdf`
- `.epub`
- `.md`
- `网页`

![preview](./preview.png)

## 启动后端

```shell
cd server
pip install -r requirements.txt
./start {OPEN_AI_KEY}
```

## 启动前端

```shell
cd client
pnpm i
pnpm dev
```
