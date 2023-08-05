from ..packages_finder import download_dependencies
from ..utils import add_download_argument
from ..utils import add_url_argument
from ..utils import add_verbose_argument
from ..utils import read_package_configuration
from ..utils import setup_build


def find_dependencies(dependencies_configs):
    packages = []

    for dependency_config in dependencies_configs:
        name = dependency_config.name

        if name == 'fiber':
            continue

        version = dependency_config.from_version
        current_version = dependency_config.version
        packages.append((name, version, current_version))

    return packages


def show(url, download):
    config = read_package_configuration()
    setup_build(download)
    dependencies_configs = download_dependencies(config, url, download)
    packages = find_dependencies(dependencies_configs)

    for name, version, _ in packages:
        if isinstance(version, str):
            version = f'"{version}"'
        else:
            version = f'{{ path = "{version["path"]}" }}'

        print(f'{name} = {version}')


def versions(url, download):
    config = read_package_configuration()
    setup_build(download)
    dependencies_configs = download_dependencies(config, url, download)
    packages = find_dependencies(dependencies_configs)

    for name, _, current_version in packages:
        print(f'{name} = "{current_version}"')


def do_deps(_parser, args, _mys_config):
    if args.versions:
        versions(args.url, args.download)
    else:
        show(args.url, args.download)


def add_subparser(subparsers):
    subparser = subparsers.add_parser(
        'deps',
        description='Show dependencies.')
    add_verbose_argument(subparser)
    add_url_argument(subparser)
    add_download_argument(subparser)
    subparser.add_argument(
        '--versions',
        action='store_true',
        help='Show all package versions currently used by this package.')
    subparser.set_defaults(func=do_deps)
