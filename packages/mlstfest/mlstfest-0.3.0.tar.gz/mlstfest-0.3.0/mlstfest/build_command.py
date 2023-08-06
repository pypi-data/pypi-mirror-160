import logging
import os
from typing import List


from mlstfest.utils import (
    create_csv,
    get_allele_sequence_path,
    get_repo_root,
    get_genome_metadata,
)

LOG = logging.getLogger(__name__)


def build_command_for_genome_metadata_submission(
    sample_id: str, organism: str
) -> List[str]:
    """
    Build the command for submission of genome metadata
    """
    repo_root = get_repo_root()
    metadata: dict = get_genome_metadata(organism=organism, sample_id=sample_id)
    path_to_csv = create_csv(metadata)
    return [
        "singularity",
        "exec",
        repo_root + "/mlstfest.sif",
        "perl",
        repo_root + "/mlstfest/rest_auth.pl",
        "--database_postfix",
        "isolates",
        "--species_name",
        organism,
        "--method",
        "POST",
        "--route",
        "submissions",
        "--arguments",
        "type=genomes",
        "--isolates_file",
        path_to_csv,
    ]


def build_command_for_assembly_upload(
    assembly: str, organism: str, submission_id: str
) -> List[str]:
    """
    Build the command to upload the assembly file
    """
    repo_root = get_repo_root()
    return [
        "singularity",
        "exec",
        "--bind",
        os.path.dirname(assembly),
        repo_root + "/mlstfest.sif",
        "perl",
        repo_root + "/mlstfest/rest_auth.pl",
        "--database_postfix",
        "isolates",
        "--species_name",
        organism,
        "--method",
        "POST",
        "--route",
        "submissions/" + submission_id + "/files",
        "--arguments",
        "filename=" + os.path.basename(assembly),
        "--file",
        assembly,
    ]


def build_command_for_allele_upload(
    assembly: str, organism: str, locus: str
) -> List[str]:
    """
    Build the command to upload an allele sequence
    """
    repo_root = get_repo_root()
    allele_sequence_path: str = get_allele_sequence_path(
        assembly=assembly, organism=organism, locus=locus
    )
    return [
        "singularity",
        "exec",
        "--bind",
        os.path.dirname(allele_sequence_path),
        repo_root + "/mlstfest.sif",
        "perl",
        repo_root + "/mlstfest/rest_auth.pl",
        "--database_postfix",
        "seqdef",
        "--species_name",
        organism,
        "--method",
        "POST",
        "--route",
        "submissions",
        "--arguments",
        "type=alleles&locus="
        + locus
        + "&assembly=de novo&technology=Illumina&software=Spades&read_length=150&coverage=>100x",
        "--sequence_file",
        allele_sequence_path,
    ]


def build_command_for_adding_comment(
    submission_id: str, associated_submission_id: str, comment_type: str, organism: str
) -> List[str]:
    """
    Build the command to add comment to a submission
    """
    repo_root = get_repo_root()

    if comment_type == "allele_upload":
        message = "message=Associated to genome upload with submission id: "
        db_postfix = "seqdef"
    elif comment_type == "profile_upload":
        message = "message=Associated to genome upload with submission id: "
        db_postfix = "seqdef"

    return [
        "singularity",
        "exec",
        repo_root + "/mlstfest.sif",
        "perl",
        repo_root + "/mlstfest/rest_auth.pl",
        "--database_postfix",
        db_postfix,
        "--species_name",
        organism,
        "--method",
        "POST",
        "--route",
        "submissions/" + submission_id + "/messages",
        "--arguments",
        message + associated_submission_id,
    ]


def build_command_for_submission_check(
    submission_id: str, organism: str, db_postfix: str
) -> List[str]:
    """
    Build the command to check what is submitted under a submission id
    """
    repo_root = get_repo_root()

    return [
        "singularity",
        "exec",
        repo_root + "/mlstfest.sif",
        "perl",
        repo_root + "/mlstfest/rest_auth.pl",
        "--database_postfix",
        db_postfix,
        "--species_name",
        organism,
        "--method",
        "GET",
        "--route",
        "submissions/" + submission_id,
    ]


def download_fasta(organism: str, locus: str) -> List[str]:
    repo_root = get_repo_root()

    return [
        "curl",
        "https://rest.pubmlst.org/db/pubmlst_"
        + organism
        + "_seqdef/loci/"
        + locus
        + "/alleles_fasta",
        "-o",
        repo_root + "/databases/" + organism + "/" + locus + ".fasta",
    ]


def build_blastdb(organism: str, locus: str) -> List[str]:
    repo_root = get_repo_root()

    return [
        "singularity",
        "exec",
        repo_root + "/mlstfest.sif",
        "makeblastdb",
        "-in",
        repo_root + "/databases/" + organism + "/" + locus + ".fasta",
        "-dbtype",
        "nucl",
        "-out",
        repo_root + "/databases/" + organism + "/" + locus + ".db",
    ]
