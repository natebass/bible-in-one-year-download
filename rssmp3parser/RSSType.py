rss_type: dict = {
    'Bible in One Year': 'bioy',
    'Unknown RSS Type': 'unknown'
}


def parse_rss_type(rss_type_input):
    match rss_type_input:
        case None:
            return rss_type["Bible in One Year"]
        case "Bible in One Year":
            return rss_type["Bible in One Year"]
        case "bioy":
            return rss_type["Bible in One Year"]
        case _:
            return rss_type["Bible in One Year"]
