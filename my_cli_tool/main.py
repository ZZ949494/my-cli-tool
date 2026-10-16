import typer

app = typer.Typer(help="一个简单实用的命令行工具")


@app.command()
def hello(name: str = typer.Argument("世界", help="要问候的名字")):
    """打印一句问候语"""
    typer.echo(f"你好, {name}!")


@app.command()
def version():
    """查看版本号"""
    from my_cli_tool import __version__
    typer.echo(f"my-cli-tool v{__version__}")


if __name__ == "__main__":
    app()
