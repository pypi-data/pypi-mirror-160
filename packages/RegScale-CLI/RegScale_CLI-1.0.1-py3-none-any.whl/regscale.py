#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

############################################################
# Imports
############################################################
import click
import app.login as lg
import app.healthcheck as hc
from app.oscal import oscal
from app.wiz import wiz
from app.migrations import migrations
from app.ad import ad
from app._version import __version__

############################################################
# CLI Command Definitions
############################################################
@click.group()
def cli():
    pass


# About function
@cli.command()
def about():
    """Provides information about the CLI and its current version."""
    click.echo("RegScale CLI Version: " + __version__)
    click.echo("Author: J. Travis Howerton (thowerton@regscale.com)")
    click.echo("Copyright: RegScale Incorporated")
    click.echo("Website: https://www.regscale.com")
    click.echo("Read the CLI Docs: https://regscale.com/documentation/cli-overview")


# Log into RegScale to get a token
@cli.command()
@click.option(
    "--username", prompt="Enter your RegScale User Name", help="RegScale User Name"
)
@click.option(
    "--password",
    prompt="Enter your RegScale Password",
    hide_input=True,
    help="RegScale Password",
)
def login(username, password):
    """Logs the user into their RegScale instance"""
    lg.login(username, password)


# Check the health of the RegScale Application
@cli.command()
def healthcheck():
    """Monitoring tool to check the health of the RegScale instance"""
    hc.status()


# add OSCAL support
cli.add_command(oscal)

# add Wiz support
cli.add_command(wiz)

# add data migration support
cli.add_command(migrations)

# add Azure Active Directory (AD) support
cli.add_command(ad)

# start function for the CLI
if __name__ == "__main__":
    cli()
