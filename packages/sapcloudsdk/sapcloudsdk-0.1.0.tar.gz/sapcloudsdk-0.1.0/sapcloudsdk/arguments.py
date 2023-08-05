from argparse import ArgumentParser, BooleanOptionalAction

parser = ArgumentParser(description="Work in progress for Innovator Challenge 2022")
parser.add_argument("--verbose", "-v", dest="verbose", action="count", default=0)
parser.add_argument(
    "--search",
    "-s",
    dest="search",
    help="The GH API search term",
    default="sap-cloud-sdk",
)
parser.add_argument(
    "--filename",
    "-f",
    dest="filename",
    help="Which files to consider",
    default="package.json",
)
parser.add_argument(
    "--api",
    "-a",
    dest="api",
    help="Base URL of the GH API",
    default="https://api.github.com",
)
parser.add_argument(
    "--language",
    "-l",
    dest="languages",
    action="append",
    help="Which languages are considered relevant e.g. JavaScript, Java, TypeScript, ...",
    default=[],
)
parser.add_argument(
    "--user",
    "-u",
    dest="user",
    help="Name of the environment variable of the GH user",
    default="GH_USER",
)
parser.add_argument(
    "--token",
    "-t",
    dest="token",
    help="Name of the environment variable storing the GH token",
    default="GH_TOKEN",
)
parser.add_argument(
    "--verify",
    dest="verify",
    action=BooleanOptionalAction,
    help="Should check SSL certificates",
    default=True,
)
parser.add_argument(
    "--load-from",
    dest="from_file",
    help="File from which to read results",
    default="code_search.json",
)
parser.add_argument(
    "--save-to",
    dest="to_file",
    help="File to which results are written",
    default="code_search.json",
)
parser.add_argument(
    "--save",
    dest="save",
    action=BooleanOptionalAction,
    help="Should file be written",
    default=True,
)

args = parser.parse_args()
