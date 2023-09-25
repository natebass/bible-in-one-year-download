rss_type: dict = {
    'Bible in One Year': 'bioy',
    'Unknown RSS Type': 'unknown'
}


def parse_rss_type(rss_type_input: str):
    """The RSS type is an identifier usually unique to the feed's name.
    NOTE: This needs to be refactored to a better way of handling default and friendly names for RSS soureces.
    :param rss_type_input: str
    :return: str
    """
    match rss_type_input:
        case None:
            return rss_type["Bible in One Year"]
        case "Bible in One Year":
            return rss_type["Bible in One Year"]
        case "bioy":
            return rss_type["Bible in One Year"]
        case _:
            return rss_type["Bible in One Year"]
