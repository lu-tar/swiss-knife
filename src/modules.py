import typer 
from typing_extensions import Annotated
cli = typer.Typer()

@cli.command()
def hello(name: str):
    print(f"Hello {name}")

@cli.command()
def goodbye(
    name: Annotated[str, typer.Argument()], 
    formal: Annotated[bool, typer.Option("--formal", "-f")] = False,
    count: Annotated[int, typer.Option("--count", "-c", help="Number of times to print the message")] = 1,
    ):
    if formal:
        print(f"{count}")
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(count)
        for i in range(count):
            print(f"Bye {name}!")