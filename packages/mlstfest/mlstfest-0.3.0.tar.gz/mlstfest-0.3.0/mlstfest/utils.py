import logging
import subprocess
import traceback
from typing import List

import pandas as pd
import os
import re
from datetime import date
from subprocess import CalledProcessError

import typer

from configs.genome_metadata_configs import staphylococcus_aureus_dict, test_dict

LOG = logging.getLogger(__name__)


def run_command(cmd: list[str], dry_run: bool) -> str:
    """
    Returns the output from a command executed in the shell
    """
    curated_command = " ".join(cmd)
    typer.echo("Running command: %s" % curated_command)
    if dry_run:
        typer.echo("Dry run: process call will not be executed!")
        return "No real output to return, this is a dry run"
    try:
        output = subprocess.check_output(cmd, shell=False)
    except CalledProcessError as err:
        LOG.error("Error - {} ".format(traceback.format_exc()))
        raise err
    return output.decode("utf-8")


def get_submission_id(output: str) -> str:
    """
    Retrieve submission id from output
    """
    # searching for submission id in output
    submission_id: str = re.search(r"(BIGSdb.*(?='))", output)

    # checking if the regex output is None
    if submission_id is None:
        typer.echo("Submission id is not found in output")
        exit()
    else:
        # accessing the string that the regex search found with .group() function
        submission_id = submission_id.group()

    return submission_id


def create_csv(metadata: dict) -> str:
    # create a dynamic filename
    repo_root = get_repo_root()

    # check if temp folder exists
    if not os.path.isdir(repo_root + "/temp"):
        os.mkdir(repo_root + "/temp")

    # create, save and echo genome_metadata_csv
    genome_metadata_path = (
        repo_root + "/temp/" + metadata["isolate"] + "_genome_metadata.csv"
    )
    metadata = pd.Series(metadata).to_frame().transpose()
    metadata.to_csv(genome_metadata_path, index=False, sep="\t")
    csv_content = run_command(["cat", genome_metadata_path], dry_run=False)
    typer.echo("Tab separated file with metadata created:")
    typer.echo(csv_content)

    return str(genome_metadata_path)


def reverse_complement(sequence: str) -> str:
    nucl_translation = {"A": "T", "C": "G", "G": "C", "T": "A"}
    return "".join(nucl_translation[n] for n in reversed(sequence))


def build_blast_search(assembly: str, organism: str, locus: str) -> List[str]:
    repo_root = get_repo_root()

    # check if temp folder exists
    if not os.path.isdir(repo_root + "/temp"):
        os.mkdir(repo_root + "/temp")

    return [
        "singularity",
        "exec",
        "--bind",
        os.path.dirname(assembly),
        "--bind",
        repo_root + "/temp/",
        repo_root + "/mlstfest.sif",
        "blastn",
        "-query",
        assembly,
        "-db",
        repo_root + "/databases/" + organism + "/" + locus + ".db",
        "-out",
        repo_root + "/temp/" + organism + "_vs_" + locus + ".blastn",
        "-task",
        "megablast",
        "-num_threads",
        "1",
        "-outfmt",
        "7 sstart send qseq",
    ]


def parsing_blastn(blastn_path: str) -> str:
    parsed_list: List[str] = []

    # open file to parse
    file = open(blastn_path, "r")
    lines = file.readlines()
    file.close()

    # loop through the lines until the first blastn hit
    for line in lines:
        if line[0] != "#":
            parsed_list = line.split()
            break

    # check if reversed complement is needed
    if int(parsed_list[0]) > int(parsed_list[1]):
        locus_sequence = reverse_complement(parsed_list[2])
    else:
        locus_sequence = parsed_list[2]

    return locus_sequence


def get_allele_sequence_path(assembly: str, organism: str, locus: str) -> str:
    repo_root = get_repo_root()

    blast_command = build_blast_search(
        assembly=assembly, organism=organism, locus=locus
    )
    run_command(blast_command, False)

    blastn_path = repo_root + "/temp/" + organism + "_vs_" + locus + ".blastn"
    locus_sequence: str = parsing_blastn(blastn_path)

    fasta_file = repo_root + "/temp/" + organism + "_" + locus + ".fasta"
    file = open(fasta_file, "w")
    file.write(">" + organism + locus + "\n")
    file.write(locus_sequence + "\n")
    file.close()

    return fasta_file


def get_repo_root() -> str:
    repo_root = run_command(
        ["git", "rev-parse", "--show-toplevel"], dry_run=False
    ).rstrip()

    return repo_root


def get_genome_metadata(organism: str, sample_id: str) -> dict:
    # choose correct metadata config
    if organism == "saureus":
        genome_metadata = staphylococcus_aureus_dict
    elif organism == "test":
        genome_metadata = test_dict
    else:
        typer.echo("Organism name not supported")
        exit()

    # add sample related metadata
    genome_metadata["isolate"] = sample_id
    genome_metadata["year"] = str(date.today().year)
    genome_metadata["assembly_filename"] = sample_id + "_contigs.fasta"

    # add only relevant columns to final metadata dict
    genome_metadata_final = {}
    for key, value in genome_metadata.items():
        if value != "":
            genome_metadata_final[key] = value

    return genome_metadata_final
