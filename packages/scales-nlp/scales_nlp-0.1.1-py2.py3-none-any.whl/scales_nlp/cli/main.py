import click
from scales_nlp.cli.configure import configure
from scales_nlp.cli.train import train

@click.group()
def main():
    pass

main.add_command(configure)
main.add_command(train)

if __name__=='__main__':
    main()