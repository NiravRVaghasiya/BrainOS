"""BrainOS CLI - Install brain-inspired plugins into your AI project."""

import os
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from brainos.plugins import PLUGINS
from brainos.generator import generate_plugin, generate_config, generate_test

console = Console()

BANNER = """
[bold cyan]BrainOS[/bold cyan] - Brain-inspired memory architecture for AI agents
[dim]Install neuroscience-backed components into your project.[/dim]
"""


@click.group()
@click.version_option(version="1.0.0", prog_name="brainos")
def main():
    """BrainOS - Brain-inspired memory plugins for AI agents."""
    pass


@main.command(name="list")
def list_plugins():
    """List all available plugins."""
    console.print(BANNER)
    table = Table(title="Available Plugins", show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=3)
    table.add_column("Plugin", style="cyan", min_width=20)
    table.add_column("Brain Analog", style="green")
    table.add_column("Savings", style="yellow", width=12)
    table.add_column("Description", style="white")

    for i, (name, info) in enumerate(PLUGINS.items(), 1):
        table.add_row(str(i), name, info["brain_analog"], info["token_savings"], info["description"])

    console.print(table)
    console.print("\n[dim]Install: brainos add <plugin-name>[/dim]")


@main.command()
@click.argument("plugin_name")
@click.option("--path", "-p", default=".", help="Target directory")
@click.option("--with-tests", is_flag=True, help="Include test file")
@click.option("--with-config", is_flag=True, help="Include YAML config")
def add(plugin_name, path, with_tests, with_config):
    """Install a plugin into your project."""
    if plugin_name == "all":
        for name in PLUGINS:
            _install_one(name, path, with_tests, with_config)
        console.print(f"\n[bold green]All {len(PLUGINS)} plugins installed.[/bold green]")
        return

    if plugin_name not in PLUGINS:
        console.print(f"[red]Unknown plugin: {plugin_name}[/red]")
        console.print(f"[dim]Available: {', '.join(PLUGINS.keys())}[/dim]")
        raise SystemExit(1)

    _install_one(plugin_name, path, with_tests, with_config)


def _install_one(name, path, with_tests, with_config):
    info = PLUGINS[name]
    target = os.path.join(path, "brainos_plugins")
    os.makedirs(target, exist_ok=True)

    # Write __init__.py
    init_path = os.path.join(target, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("# BrainOS plugins\n")

    # Write plugin module
    filename = f"{name.replace('-', '_')}.py"
    filepath = os.path.join(target, filename)
    with open(filepath, "w") as f:
        f.write(generate_plugin(name))
    console.print(f"[green]  +[/green] {filepath}")

    if with_config:
        cfg_dir = os.path.join(path, "config")
        os.makedirs(cfg_dir, exist_ok=True)
        cfg_path = os.path.join(cfg_dir, f"{name.replace('-', '_')}.yaml")
        with open(cfg_path, "w") as f:
            f.write(generate_config(name))
        console.print(f"[green]  +[/green] {cfg_path}")

    if with_tests:
        test_dir = os.path.join(path, "tests")
        os.makedirs(test_dir, exist_ok=True)
        test_path = os.path.join(test_dir, f"test_{name.replace('-', '_')}.py")
        with open(test_path, "w") as f:
            f.write(generate_test(name))
        console.print(f"[green]  +[/green] {test_path}")

    console.print(f"[bold green]  Installed: {name}[/bold green] [dim]({info['brain_analog']})[/dim]")


@main.command()
@click.argument("plugin_name")
def info(plugin_name):
    """Show details about a plugin."""
    if plugin_name not in PLUGINS:
        console.print(f"[red]Unknown: {plugin_name}[/red]")
        raise SystemExit(1)
    p = PLUGINS[plugin_name]
    deps = ", ".join(p["dependencies"]) if p["dependencies"] else "none"
    panel = Panel(
        f"[bold]{p['description']}[/bold]\n\n"
        f"[cyan]Brain Analog:[/cyan]  {p['brain_analog']}\n"
        f"[yellow]Token Savings:[/yellow] {p['token_savings']}\n"
        f"[green]Dependencies:[/green]  {deps}\n\n"
        f"[dim]Install: brainos add {plugin_name} --with-config --with-tests[/dim]",
        title=f"brainos: {plugin_name}",
        border_style="cyan"
    )
    console.print(panel)


@main.command()
@click.option("--path", "-p", default=".", help="Target directory")
def init(path):
    """Initialize a BrainOS-powered project structure."""
    console.print(BANNER)
    for d in ["brainos_plugins", "config", "tests"]:
        os.makedirs(os.path.join(path, d), exist_ok=True)

    with open(os.path.join(path, "brainos_plugins", "__init__.py"), "w") as f:
        f.write("# BrainOS plugins\n")

    with open(os.path.join(path, "config", "brainos.yaml"), "w") as f:
        f.write("# BrainOS Configuration\nbrainos:\n  token_budget: 8000\n  embedding_model: all-MiniLM-L6-v2\n")

    console.print("[green]Project initialized.[/green]")
    console.print("\n  brainos_plugins/   <- Plugin code")
    console.print("  config/            <- YAML configs")
    console.print("  tests/             <- Tests")
    console.print("\n[dim]Next: brainos add sensory-gate --with-config[/dim]")


if __name__ == "__main__":
    main()
