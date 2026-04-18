import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rag.pipeline import rag_pipeline
from ingestion.ingest import ingest_file, ingest_directory
from knowledge.graph import graph_builder
from pathlib import Path
import sys

console = Console()

def main_cli():
    parser = argparse.ArgumentParser(description="Memora - Personal Knowledge Assistant")
    subparsers = parser.add_subparsers(dest="command")

    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a file or directory")
    ingest_parser.add_argument("path", type=str, help="Path to file or directory")

    # Query command
    query_parser = subparsers.add_parser("query", help="Ask a question")
    query_parser.add_argument("question", type=str, help="Your question")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Start an interactive chat")

    # Graph command
    graph_parser = subparsers.add_parser("graph", help="Build/Update knowledge graph")

    args = parser.parse_args()

    if args.command == "ingest":
        path = Path(args.path)
        if path.is_dir():
            ingest_directory(path)
        else:
            ingest_file(path)
        console.print(f"[bold green]Ingestion complete for {args.path}[/bold green]")

    elif args.command == "query":
        with console.status("[bold blue]Searching memory...[/bold blue]"):
            answer = rag_pipeline.query(args.question)
        console.print(Panel(answer, title="Memora's Response", expand=False))

    elif args.command == "chat":
        console.print("[bold cyan]Welcome to Memora Chat! Type 'exit' to quit.[/bold cyan]")
        while True:
            question = console.input("[bold yellow]Query > [/bold yellow]")
            if question.lower() in ["exit", "quit"]:
                break
            with console.status("[bold blue]Thinking...[/bold blue]"):
                answer = rag_pipeline.query(question)
            console.print(Panel(answer, title="Memora", expand=False))

    elif args.command == "graph":
        console.print("[bold blue]Building knowledge graph...[/bold blue]")
        graph_builder.save_graph()
        console.print("[bold green]Graph built successfully in data/graph.json[/bold green]")

    else:
        parser.print_help()

if __name__ == "__main__":
    main_cli()
