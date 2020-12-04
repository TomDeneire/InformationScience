"""
Helper function for MARC21 to DC conversion
"""


def table() -> dict:
    """
    Source: Library of Congress Crosswalk for MARC21 to Dublin Core
    https://www.loc.gov/marc/marc2dc.html
    """

    # Map fields to Dublin Core
    dc_contributor = ["100a", "110a", "111a", "700a", "710a", "711a", "720a"]

    dc_coverage = ["651a", "662a", "751a", "752a"]

    dc_date = ["008a", "260c", "260d", "260e", "260f", "260g"]
    # Crosswalk specification includes "10*"
    # however, actually only "100d", "100f" represent dates
    # https://www.loc.gov/marc/bibliographic/concise/bd100.html
    for prefix in ["07", "08", "09", "10"]:
        dc_date = dc_date + [prefix + str(nr) + "a" for nr in range(0, 10)]

    dc_description = [str(nr) + "a" for nr in range(500, 600)]
    for item in ["506a", "530a", "540a", "546a"]:
        dc_description.remove(item)

    dc_format = ["340a", "856q"]

    dc_identifier = ["020a", "022a", "024a", "856u"]

    dc_language = ["008a", "041a", "041b", "041d", "041e", "041f", "041g",
                   "041h", "041j", "546"]
    for prefix in ["35", "37"]:
        dc_language = dc_language + [prefix + str(nr)
                                     + "a" for nr in range(0, 10)]

    dc_publisher = ["260a", "260b"]

    dc_relation = ["530a", "787o", "787t"]
    for prefix in ["76", "77"]:
        dc_relation = dc_relation + [prefix + str(nr)
                                     + "a" for nr in range(0, 10)]

    dc_rights = ["506a", "540a"]

    dc_source = ["534t", "786o", "786t"]

    dc_subject = ["050a", "060a", "080a", "082a", "600a", "610a", "611a",
                  "630a", "650a", "653a"]

    dc_title = ["245a", "246a", "210a", "222a", "240a", "242a", "243a", "247a"]

    dc_type = ["655a"]

    # Combine mappings into table
    table = {"contributor": dc_contributor,
             "coverage": dc_coverage,
             "date": dc_date,
             "description": dc_description,
             "format": dc_format,
             "identifier": dc_identifier,
             "language": dc_language,
             "publisher": dc_publisher,
             "relation": dc_relation,
             "rights": dc_rights,
             "source": dc_source,
             "subject": dc_subject,
             "title": dc_title,
             "type": dc_type}

    return table
