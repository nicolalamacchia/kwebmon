import json
from operator import itemgetter
from itertools import tee
from typing import Optional

import jsonschema

from kwebmon_producer.json_schemas import SITES_JSON_SCHEMA


class BadSitesList(Exception):
    """
    Exception for badly formatted or invalid JSON sites list.
    """


def _first_duplicate_url(sites: list[dict]) -> Optional[str]:
    # sort by the 'url' key and get two iterators from the original one
    iter_a, iter_b = tee(sorted(sites, key=itemgetter("url")))
    # advance one iterator
    next(iter_b, None)
    # zip the two iterators and loop pairwise, now sites with the same
    # URL are adjacent
    for site_a, site_b in zip(iter_a, iter_b):
        url_a = site_a["url"]
        url_b = site_b["url"]
        if url_a == url_b:
            return url_a


def get_sites(json_file: str) -> list[dict]:
    """
    Gets the list of URLs to be monitored with RegEx patterns to be
    checked in their respective responses.

    :param json_file: the JSON file containing the sites to be monitored
    :returns: details about the sites to be monitored
    :raises BadSitesList: the input JSON is either badly formatted or invalid
    :raises FileNotFoundError: the input file does not exists
    """
    try:
        with open(json_file) as sites_list_file:
            sites_config = json.load(sites_list_file)
        jsonschema.validate(instance=sites_config, schema=SITES_JSON_SCHEMA)
    except (
        json.decoder.JSONDecodeError,
        jsonschema.ValidationError,
    ) as json_schema_error:
        raise BadSitesList(
            f"Invalid JSON file: {json_schema_error}"
        ) from json_schema_error

    sites = sites_config["sites"]
    first_duplicate = _first_duplicate_url(sites)

    try:
        assert first_duplicate is None
    except AssertionError:
        raise BadSitesList(
            f"Invalid JSON file, duplicate URL found: '{first_duplicate}'"
        )

    return sites
