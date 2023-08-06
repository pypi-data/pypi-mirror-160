from typing import Union, Optional
from warnings import warn

from gcip import Sequence
from gcip.core.cache import Cache
from gcip.addons.container.jobs import dive, crane, trivy
from gcip.addons.container.registries import Registry

"""
The following helper methods are used by multiple sequences in this package
to avoid repetition.
"""


def add_dive_scan_job_to_sequence(
    *,
    sequence: Sequence,
    dive_scan_opts: Optional[dive.ScanOpts],
    sequence_cache: Cache,
    image_name: Optional[str] = None,
) -> dive.Scan:
    if not dive_scan_opts:
        dive_scan_opts = dive.ScanOpts()

    if dive_scan_opts.image_path:
        warn(f"dive_scan_opts.image_path will be overridden by {type(sequence).__name__}'s internal cache path")
    if dive_scan_opts.image_name:
        warn(f"dive_scan_opts.image_name will be overridden by {type(sequence).__name__}.image_name")
    if dive_scan_opts.job_opts and dive_scan_opts.job_opts.cache:
        warn(f"dive_scan_opts.job_opts.cache will be overridden by {type(sequence).__name__}'s internal cache")

    dive_scan_opts.image_path = sequence_cache.paths[0]
    dive_scan_opts.image_name = image_name

    dive_scan_job = dive.Scan(**dive_scan_opts.__dict__)
    dive_scan_job.set_cache(sequence_cache)
    sequence.add_children(dive_scan_job)

    return dive_scan_job


def add_trivy_scan_job_to_sequence(
    *,
    sequence: Sequence,
    trivy_scan_opts: Optional[trivy.ScanLocalImageOpts],
    sequence_cache: Cache,
    image_name: Optional[str] = None,
) -> trivy.ScanLocalImage:
    if not trivy_scan_opts:
        trivy_scan_opts = trivy.ScanLocalImageOpts()

    if trivy_scan_opts.image_path:
        warn(f"trivy_scan_opts.image_path will be overridden by {type(sequence).__name__}'s internal cache path")
    if trivy_scan_opts.image_name:
        warn(f"trivy_scan_opts.image_name will be overridden by {type(sequence).__name__}Opts.image_name")
    if trivy_scan_opts.job_opts and trivy_scan_opts.job_opts.cache:
        warn(f"trivy_scan_opts.job_opts.cache will be overridden by {type(sequence).__name__}'s internal cache")

    trivy_scan_opts.image_path = sequence_cache.paths[0]
    trivy_scan_opts.image_name = image_name

    trivy_scan_job = trivy.ScanLocalImage(**trivy_scan_opts.__dict__)
    trivy_scan_job.set_cache(sequence_cache)
    sequence.add_children(trivy_scan_job)

    return trivy_scan_job


def add_trivy_ignore_file_check_to_sequence(
    *,
    sequence: Sequence,
    trivy_ignore_file_check_opts: Optional[trivy.TrivyIgnoreFileCheckOpts],
) -> trivy.TrivyIgnoreFileCheck:
    if not trivy_ignore_file_check_opts:
        trivy_ignore_file_check_opts = trivy.TrivyIgnoreFileCheckOpts()
    trivy_ignore_file_check_job = trivy.TrivyIgnoreFileCheck(**trivy_ignore_file_check_opts.__dict__)
    sequence.add_children(trivy_ignore_file_check_job)
    return trivy_ignore_file_check_job


def add_crane_push_job_to_sequence(
    *,
    sequence: Sequence,
    crane_push_opts: Optional[crane.PushOpts],
    sequence_cache: Cache,
    image_name: Optional[str] = None,
    image_tag: Optional[str] = None,
    registry: Union[Registry, str],
) -> crane.Push:
    if not crane_push_opts:
        crane_push_opts = crane.PushOpts()

    if crane_push_opts.dst_registry:
        warn(f"crane_push_opts.dst_registry will be overridden by {type(sequence).__name__}.dst_registry")
    if crane_push_opts.tar_path:
        warn(f"crane_push_opts.tar_path will be overridden by {type(sequence).__name__}'s internal cache path")
    if crane_push_opts.image_name:
        warn(f"crane_push_opts.image_name will be overridden by {type(sequence).__name__}.image_name")
    if crane_push_opts.image_tag:
        warn(f"crane_push_opts.image_tag will be overridden by {type(sequence).__name__}.image_tag")

    crane_push_opts.dst_registry = registry
    crane_push_opts.tar_path = sequence_cache.paths[0]
    crane_push_opts.image_name = image_name
    crane_push_opts.image_tag = image_tag

    crane_push_job = crane.Push(**crane_push_opts.__dict__)
    crane_push_job.set_cache(sequence_cache)
    sequence.add_children(crane_push_job)

    return crane_push_job
