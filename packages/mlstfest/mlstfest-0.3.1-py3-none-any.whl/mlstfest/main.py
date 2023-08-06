import logging
from typing import List

import typer

from mlstfest import __version__, __title__
from mlstfest.build_command import (
    build_command_for_genome_metadata_submission,
    build_command_for_assembly_upload,
    build_command_for_allele_upload,
    build_command_for_adding_comment,
    build_command_for_submission_check,
    download_fasta,
    build_blastdb,
)
from mlstfest.utils import run_command, get_submission_id
from configs.loci import MARKERS


app = typer.Typer()
LOG = logging.getLogger(__name__)


@app.callback()
def callback(debug: bool = False):
    """
    mlstfest - Strain type assignment to novel microbe sequences
    """
    if debug:
        typer.echo("DEBUG logging enabled")
        logging.basicConfig(level=logging.DEBUG)


@app.command()
def version():
    """
    Print the version
    """
    typer.echo("%s, version %s" % (__title__, __version__))


@app.command()
def upload_genome_metadata(
    organism: str = typer.Option(..., help="Species name"),
    sample_id: str = typer.Option(..., help="Unique sample id"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> str:
    """
    Upload genome metadata
    """
    typer.echo("Collecting metadata for sample: %s" % sample_id)
    command: List[str] = build_command_for_genome_metadata_submission(
        organism=organism, sample_id=sample_id
    )
    output: str = run_command(cmd=command, dry_run=dry_run)
    typer.echo(output)
    submission_id = get_submission_id(output=output)
    typer.echo("Genome metadata submitted with ID: %s" % submission_id)
    return submission_id


@app.command()
def upload_genome_file(
    assembly: str = typer.Option(..., help="Path to assembly"),
    organism: str = typer.Option(..., help="Species name"),
    submission_id: str = typer.Option(..., help="Submission ID (BIGSdb)"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> bool:
    """
    Upload genome file
    """
    typer.echo("Preparing upload of assembly: %s" % assembly)
    command: List[str] = build_command_for_assembly_upload(
        assembly=assembly, organism=organism, submission_id=submission_id
    )
    output: str = run_command(command, dry_run)
    typer.echo(output)
    if "'message' => 'File uploaded.'" in output:
        return True
    else:
        typer.echo("ERROR: File could not be uploaded")
        exit()


@app.command()
def upload_alleles(
    assembly: str = typer.Option(..., help="Path to assembly"),
    organism: str = typer.Option(..., help="Species name"),
    locus: str = typer.Option(..., help="Name of locus"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> str:
    """
    Upload alleles
    """
    typer.echo("Initiating allele upload")
    command: List[str] = build_command_for_allele_upload(
        assembly=assembly, organism=organism, locus=locus
    )
    output: str = run_command(command, dry_run)
    typer.echo(output)
    if not "BIGSdb" in output:
        typer.echo("ERROR: Allele could not be uploaded")
        exit()
    submission_id = get_submission_id(output=output)
    typer.echo("Allele from locus %s submitted with ID: %s" % (locus, submission_id))
    return submission_id


@app.command()
def comment_allele_upload(
    allele_submission_id: str = typer.Option(
        ..., help="Submission ID for the allele upload"
    ),
    genome_submission_id: str = typer.Option(
        ..., help="Submission ID for the genome upload"
    ),
    organism: str = typer.Option(..., help="Species name"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> bool:
    """
    Add comment to allele submission
    """
    typer.echo("Adding comment to allele submission")
    command: List[str] = build_command_for_adding_comment(
        submission_id=allele_submission_id,
        associated_submission_id=genome_submission_id,
        comment_type="allele_upload",
        organism=organism,
    )

    output: str = run_command(command, dry_run)
    typer.echo(output)
    if "'message' => 'Message added.'" in output:
        return True
    else:
        typer.echo("ERROR: Message was not successfully added allele upload")
        exit()


@app.command()
def comment_profile_upload(
    profile_submission_id: str = typer.Option(
        ..., help="Submission ID for the profile upload"
    ),
    genome_submission_id: str = typer.Option(
        ..., help="Submission ID for the genome upload"
    ),
    organism: str = typer.Option(..., help="Species name"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> bool:
    """
    Add comment to profile submission
    """
    typer.echo("Adding comment to profile submission")
    command: List[str] = build_command_for_adding_comment(
        submission_id=profile_submission_id,
        associated_submission_id=genome_submission_id,
        comment_type="profile_upload",
        organism=organism,
    )

    output: str = run_command(command, dry_run)
    typer.echo(output)
    if "'message' => 'Message added.'" in output:
        return True
    else:
        typer.echo("ERROR: Message was not successfully added to profile upload")
        exit()


@app.command()
def upload_profile():
    """
    Upload profile
    """
    typer.echo("Initiating profile upload")


@app.command()
def check_status(
    submission_id: str = typer.Option(..., help="Submission ID (BIGSdb)"),
    organism: str = typer.Option(..., help="Species name"),
    db_postfix: str = typer.Option(
        ..., help="Type name of database, possible options are: isolates or seqdef"
    ),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """
    Check status of a submission
    """
    POSSIBLE_DB_POSTFIXES = ["isolates", "seqdef"]
    if db_postfix not in POSSIBLE_DB_POSTFIXES:
        typer.echo("Invalid database postfix selected")
        exit()

    typer.echo("Querying the database for information regarding submission")
    command: List[str] = build_command_for_submission_check(
        submission_id=submission_id,
        organism=organism,
        db_postfix=db_postfix.lower(),
    )
    output: str = run_command(command, dry_run)
    typer.echo(output)


@app.command()
def upload_sequence_data():
    """
    Upload genome assembly and novel alleles, then add comments
    """
    typer.echo("Initiating upload of genome and novel alleles")


@app.command()
def get_latest_database(
    organism: str = typer.Option(..., help="Species name"),
    dry_run: bool = typer.Option(False, "--dry-run"),
):
    """
    Get latest database for specified species
    """
    typer.echo("Initiating download of database(s)")
    for locus in MARKERS[organism]:
        print(locus)
        command: List[str] = download_fasta(locus=locus, organism=organism)
        output: str = run_command(command, dry_run)
        typer.echo(output)

        command: List[str] = build_blastdb(locus=locus, organism=organism)
        output: str = run_command(command, dry_run)
        typer.echo(output)
