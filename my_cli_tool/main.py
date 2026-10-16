import os
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


@app.command("rename")
def rename_files(
    folder: str = typer.Argument(".", help="要重命名的文件夹路径"),
    prefix: str = typer.Option(None, help="给所有文件加前缀，比如 test_"),
    suffix: str = typer.Option(None, help="给所有文件加后缀（在扩展名前面），比如 _v1"),
    replace: str = typer.Option(None, help="替换文件名中的文字，格式：旧文字=新文字"),
    ext: str = typer.Option(None, help="只处理某类文件，比如 .py 或 .jpg"),
    dry_run: bool = typer.Option(False, "--dry-run", help="只预览不实际改名"),
):
    """批量重命名文件夹里的文件"""
    if not any([prefix, suffix, replace]):
        typer.echo("错误：至少要指定 --prefix / --suffix / --replace 其中一个")
        typer.echo("示例：my-cli-tool rename . --prefix test_ --ext .jpg")
        raise typer.Exit(1)

    if replace and "=" not in replace:
        typer.echo("错误：--replace 格式应该是 旧文字=新文字，比如 --replace 报告=周报")
        raise typer.Exit(1)

    if not os.path.isdir(folder):
        typer.echo(f"错误：文件夹不存在 - {folder}")
        raise typer.Exit(1)

    renamed = 0
    skipped = 0

    for filename in sorted(os.listdir(folder)):
        filepath = os.path.join(folder, filename)
        if not os.path.isfile(filepath):
            continue

        name, extension = os.path.splitext(filename)

        if ext and not extension.lower() == ext.lower():
            continue

        new_name = name

        if prefix:
            new_name = prefix + new_name

        if suffix:
            new_name = new_name + suffix

        if replace:
            old, new = replace.split("=", 1)
            new_name = new_name.replace(old, new)

        new_filename = new_name + extension

        if new_filename == filename:
            skipped += 1
            continue

        new_filepath = os.path.join(folder, new_filename)

        if os.path.exists(new_filepath):
            typer.echo(f"跳过（目标已存在）：{filename} -> {new_filename}")
            skipped += 1
            continue

        action = "[预览]" if dry_run else "[重命名]"
        typer.echo(f"{action} {filename}  ->  {new_filename}")

        if not dry_run:
            os.rename(filepath, new_filepath)

        renamed += 1

    typer.echo("-" * 40)
    mode = "预览模式（未实际修改）" if dry_run else "完成"
    typer.echo(f"{mode}：处理 {renamed} 个，跳过 {skipped} 个")


if __name__ == "__main__":
    app()
