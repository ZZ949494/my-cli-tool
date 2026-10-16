# my-cli-tool

一个简单实用的命令行工具脚手架，基于 Python + Typer。

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行

```bash
python -m my_cli_tool.main hello
```

### 打包安装为全局命令

```bash
pip install -e .
my-cli-tool hello
```

## 功能

- `hello` - 打印问候语
- 后续按需添加子命令

## License

MIT
