"""
Packaging utilities
"""

import argparse
import glob
import os
import shutil
import subprocess
from subprocess import CalledProcessError
import sys
import textwrap
from typing import (
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
)

from pkginfo import Distribution, SDist, Wheel
import requests
from setuptools.extern.packaging.version import LegacyVersion, parse
import setuptools_scm
import xmltodict


try:
    import keyring
    _HAVE_KEYRING = True
except ModuleNotFoundError:
    _HAVE_KEYRING = False


class SmokeCheck(Exception):
    """Generic exception used to indicated a failing pre-condition."""


# Copied from qemu.git/python/qemu/utils/__init__.py 2022-07-13
# pylint: disable=too-many-arguments
def add_visual_margin(
        content: str = '',
        width: Optional[int] = None,
        name: Optional[str] = None,
        padding: int = 1,
        upper_left: str = '┏',
        lower_left: str = '┗',
        horizontal: str = '━',
        vertical: str = '┃',
) -> str:
    """
    Decorate and wrap some text with a visual decoration around it.

    This function assumes that the text decoration characters are single
    characters that display using a single monospace column.

    ┏━ Example ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ┃ This is what this function looks like with text content that's
    ┃ wrapped to 66 characters. The right-hand margin is left open to
    ┃ accommodate the occasional unicode character that might make
    ┃ predicting the total "visual" width of a line difficult. This
    ┃ provides a visual distinction that's good-enough, though.
    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    :param content: The text to wrap and decorate.
    :param width:
        The number of columns to use, including for the decoration
        itself. The default (None) uses the the available width of the
        current terminal, or a fallback of 72 lines. A negative number
        subtracts a fixed-width from the default size. The default obeys
        the COLUMNS environment variable, if set.
    :param name: A label to apply to the upper-left of the box.
    :param padding: How many columns of padding to apply inside.
    :param upper_left: Upper-left single-width text decoration character.
    :param lower_left: Lower-left single-width text decoration character.
    :param horizontal: Horizontal single-width text decoration character.
    :param vertical: Vertical single-width text decoration character.
    """
    if width is None or width < 0:
        avail = shutil.get_terminal_size(fallback=(72, 24))[0]
        if width is None:
            _width = avail
        else:
            _width = avail + width
    else:
        _width = width

    prefix = vertical + (' ' * padding)

    def _bar(name: Optional[str], top: bool = True) -> str:
        ret = upper_left if top else lower_left
        if name is not None:
            ret += f"{horizontal} {name} "

        filler_len = _width - len(ret)
        ret += f"{horizontal * filler_len}"
        return ret

    def _wrap(line: str) -> str:
        return os.linesep.join(
            textwrap.wrap(
                line, width=_width - padding, initial_indent=prefix,
                subsequent_indent=prefix, replace_whitespace=False,
                drop_whitespace=True, break_on_hyphens=False)
        )

    return os.linesep.join((
        _bar(name, top=True),
        os.linesep.join(_wrap(line) for line in content.splitlines()),
        _bar(None, top=False),
    ))


# Copied from qemu.git/python/qemu/utils/__init__.py 2022-07-13
class VerboseProcessError(CalledProcessError):
    """
    The same as CalledProcessError, but more verbose.

    This is useful for debugging failed calls during test executions.
    The return code, signal (if any), and terminal output will be displayed
    on unhandled exceptions.
    """
    def summary(self) -> str:
        """Return the normal CalledProcessError str() output."""
        return super().__str__()

    def __str__(self) -> str:
        lmargin = '  '
        width = -len(lmargin)
        sections = []

        # Does self.stdout contain both stdout and stderr?
        has_combined_output = self.stderr is None

        name = 'output' if has_combined_output else 'stdout'
        if self.stdout:
            sections.append(add_visual_margin(self.stdout, width, name))
        else:
            sections.append(f"{name}: N/A")

        if self.stderr:
            sections.append(add_visual_margin(self.stderr, width, 'stderr'))
        elif not has_combined_output:
            sections.append("stderr: N/A")

        return os.linesep.join((
            self.summary(),
            textwrap.indent(os.linesep.join(sections), prefix=lmargin),
        ))


def git(args: Sequence[str], check: bool = True
        ) -> 'subprocess.CompletedProcess[str]':
    """
    Make a call to git and capture the output.

    :param args: Arguments to git, as a single string.
    :param check: Raise an exception when the RC is nonzero.

    :return: a CompletedProcess instance.
    """
    full_args = ['git'] + list(args)
    subp = subprocess.run(
        full_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        check=False
    )

    if check and subp.returncode or (subp.returncode < 0):
        raise VerboseProcessError(
            subp.returncode, full_args,
            output=subp.stdout,
            stderr=subp.stderr,
        )

    return subp


def git_str(args: Sequence[str], check: bool = True) -> str:
    """
    Make a call to git and capture the output as a single string.

    :param args: Arguments to git, as a single string.
    :param check: Raise an exception when the RC is nonzero.

    :return: stdout from the git process.
    """
    return git(args, check).stdout.strip()


def run(args: Sequence[str], separator: bool = True) -> None:
    """
    Run a subprocess without redirecting streams.

    Useful for interactive processes, or when we wish to see all of the
    procedural output from a git routine.

    :param separator: Print a little ascii separator to box the output.
    """
    # This won't always produce a "legal" CLI, but it's just for display.
    print('> ' + " ".join(args))
    if separator:
        print("-" * 80)
    sys.stdout.flush()
    try:
        subprocess.run(args, check=True)
    finally:
        sys.stdout.flush()
        if separator:
            print("-" * 80)
            print("")


def interactive_confirm(prompt: str) -> None:
    """Force an interactive confirmation before proceeding."""
    while True:
        print(prompt + " (Y/N)")
        answ = input("> ").lower()
        if answ == 'y':
            break
        if answ == 'n':
            raise SmokeCheck("Aborted.")
        print("Please answer 'y' for yes or 'n' for no.\n")


def check_clean_git(check: bool = True) -> Dict[str, List[str]]:
    """
    Check for any loose files in the repo.

    Checks for modified, deleted, untracked, or uncommitted files.

    :param check: Raise an exception when the repo is not clean.

    :return:
        A dict, each key records the files from that category of loose
        file. Empty when the repo is clean.
    """
    files: Dict[str, List[str]] = {}

    res = git(('ls-files', '--modified'))
    modified = res.stdout.splitlines()
    if modified:
        files['modified'] = modified

    res = git(('ls-files', '--other', '--exclude-standard'))
    untracked = res.stdout.splitlines()
    if untracked:
        files['untracked'] = untracked

    res = git(('ls-files', '--deleted'))
    deleted = res.stdout.splitlines()
    if deleted:
        files['deleted'] = deleted

    res = git(('diff', '--staged', '--name-only'))
    staged = res.stdout.splitlines()
    if staged:
        files['staged'] = staged

    if files and check:
        raise SmokeCheck(f"Repository is not clean. {files}")

    return files


def do_tag(remote: str) -> str:
    """
    Perform smoke checks and interactively perform the actual tagging.

    :param remote: The name of the remote we intend to push to.

    :return: The new tag name.
    """
    try:
        tag = git_str(('describe', '--exact-match', '--tags'))
        raise SmokeCheck(f"Commit already has tag '{tag}'")
    except subprocess.CalledProcessError:
        pass

    try:
        last_tag = git_str(('describe', '--abbrev=0'))
    except subprocess.CalledProcessError:
        last_tag = "(None found!)"
    print(f"Last known version tag: {last_tag}")

    current_vers = setuptools_scm.get_version()
    print(f"Current version: {current_vers}")

    answ = input("Please input the new version: ").strip()
    version = parse(answ)
    if isinstance(version, LegacyVersion):
        raise SmokeCheck(f"'{version}' is not a PEP 440 compliant version.")
    print(f"New version: {version}")
    tag = f"v{version}"
    print(f"New tag: '{tag}'")

    # Ensure this tag is not in use on the remote *before* we tag.
    # Note, ls-remote does contact the remote and get fresh tag data.
    remote_tags = git(('ls-remote', '--tags', remote))
    for line in remote_tags.stdout.splitlines():
        entry = line.split()
        assert len(entry) == 2

        if entry[1] == f"refs/tags/{tag}":
            raise SmokeCheck(
                f"Tag '{tag}' already defined on remote '{remote}'.")

    # Tag the current commit (Allow for interactive signing):
    run(('git', 'tag', '-s', tag, '-m', tag), separator=False)

    return tag


def git_tag_push(remote: str, tag: str) -> None:
    """
    Perform the actual tag push to the remote.

    :param remote: The remote to push to.
    :param tag: The tag to push.
    """
    # Dry run: try to push the tag. Allow interactivity for auth etc.
    print("Dry run:")
    run(('git', 'push', '-v', remote, tag, '--dry-run'))

    interactive_confirm(f"Should we proceed to push the tag to '{remote}'?")

    # This time for real!
    print("Pushing:")
    run(('git', 'push', '-v', remote, tag))


def check_dist_files() -> Tuple[str, str, List[str]]:
    """
    Check the integrity of distribution files.

    Checks the integrity and versions of built distribution
    files. Ensure all distribution files have PEP 440 compliant
    versions. Ensure all distribution files are for the same version.

    :return: The version shared by all distfiles.
    """
    print("Checking integrity of dist files ...")
    distfiles = glob.glob('dist/*')
    if not distfiles:
        raise SmokeCheck("No distribution files found.")
    run([sys.executable, '-m', 'twine', 'check', '--strict'] + distfiles)

    print("Checking versions of dist files ...")
    dist: Distribution
    versions = set()
    names = set()
    for file in distfiles:
        if file.endswith('.whl'):
            dist = Wheel(file)
        elif file.endswith('.tar.gz'):
            dist = SDist(file)
        else:
            raise SmokeCheck(f"Unrecognized dist file type: '{file}'")

        version = parse(dist.version)
        if isinstance(version, LegacyVersion):
            raise SmokeCheck(
                f"'{version}' of file '{file}' "
                "is not a PEP 440 compliant version."
            )
        versions.add(str(version))
        names.add(dist.name)

    assert versions
    if len(versions) != 1:
        verstr = ", ".join(versions)
        raise SmokeCheck(
            "Expected only one version, "
            f"found {len(versions)}; {verstr}"
        )

    assert names
    if len(names) != 1:
        namestr = ", ".join(names)
        raise SmokeCheck(
            "Expected only one package name, "
            f"found {len(names)}; {namestr}"
        )

    return versions.pop(), names.pop(), distfiles


def check_published_versions(
        repo: str, pkg_name: str, pkg_version: str) -> None:
    """
    Check PyPI or Test PyPI for package conflicts.

    :param repo: pypi.org or test.pypi.org
    :param pkg_name: Package name to be published
    :param pkg_version: Package version to be published
    """
    print(f"Checking for version collisions on {repo} ...")
    url = f"https://{repo}/rss/project/{pkg_name}/releases.xml"
    req = requests.get(url)
    req.raise_for_status()

    data = xmltodict.parse(req.content)
    items = data['rss']['channel']['item']
    if not isinstance(items, list):
        items = [items]

    for release in items:
        if release['title'] == pkg_version:
            raise SmokeCheck(
                f"Package version ('{pkg_version}') "
                f"is already present on {repo}: {release['link']}"
            )


def make_tag() -> None:
    """Interactively create and then push a new tag."""
    check_clean_git()
    print("Repository is clean.")

    ref = git_str(('rev-parse', '--symbolic-full-name', '@{push}'))
    print(f"Push target is currently '{ref}'.")

    path = ref.split('/')
    assert path[0] == 'refs'
    assert path[1] == 'remotes'
    remote = path[2]
    print(f"Push remote determined to be '{remote}'.")

    tag = do_tag(remote)
    try:
        git_tag_push(remote, tag)
    except:
        run(('git', 'tag', '--delete', tag))
        raise

    print("All set!")


def build() -> None:
    """
    Build distribution files.

    Ensures the repo is clean of loose files, and performs a check using
    twine on the built files.
    """
    print("Building ...")
    check_clean_git()
    print("Repository is clean.")

    print("Building distfiles ...")
    run((sys.executable, '-m', 'build'))

    check_dist_files()

    print("OK!")


def publish(test: bool) -> None:
    """
    Take built dist files and publish them to PyPI.

    Function will interactively prompt before the final submission.

    :param test: Publish to test.pypi.org instead of pypi.org.
    """
    repo = 'test.pypi.org' if test else 'pypi.org'

    print(f"Publishing ({repo}) ...")
    # Note, this doesn't find .gitignore items, so dist/* is OK.
    check_clean_git()
    print("Repository is clean.")

    pkg_version, pkg_name, distfiles = check_dist_files()

    # Check for collisions on PyPI. Check the test bed site if appropriate,
    # but always check the production site.

    check_published_versions('pypi.org', pkg_name, pkg_version)
    if test:
        check_published_versions('test.pypi.org', pkg_name, pkg_version)

    env = os.environ.copy()
    if test:
        env['TWINE_REPOSITORY'] = 'testpypi'
    env['TWINE_USERNAME'] = os.environ.get('TWINE_USERNAME', '__token__')

    if not env.get('TWINE_PASSWORD') and _HAVE_KEYRING:
        user = env['TWINE_USERNAME']
        # Tokens may be defined per-package; so don't pollute the namespace.
        if user == '__token__':
            user = f"{pkg_name}:__token__"
        env['TWINE_PASSWORD'] = keyring.get_password(
            f"https://{repo}/legacy/", user) or ''

    if not env.get('TWINE_PASSWORD'):
        emsg = "TWINE_PASSWORD was unset, cannot continue."
        emsg += f"\n  Maybe try: keyring set https://{repo}/legacy/ '{user}'"
        raise SmokeCheck(emsg)

    interactive_confirm(f"Publish '{pkg_name}' v{pkg_version} to {repo}?")

    subprocess.run(
        [sys.executable, '-m', 'twine',
         'upload', '--sign', '--non-interactive', '--verbose'] + distfiles,
        env=env,
        check=True,
    )

    print("Success!")


def main() -> None:
    """Main command-line interface."""
    parser = argparse.ArgumentParser(
        description="Python package publishing helper.",
    )
    subparsers = parser.add_subparsers(
        title='action',
        dest='action',
        required=True,
        help='Action to perform',
        metavar='action',
    )

    subparsers.add_parser('tag', help="Tag a new release.")
    subparsers.add_parser('build', help="Build a new release.")
    sub = subparsers.add_parser(
        'publish',
        help="Publish a new release to PyPI."
    )
    sub.add_argument(
        '--test',
        action='store_true',
        help="Publish to test.pypi.org instead of PyPI.",
    )

    args = parser.parse_args()

    try:
        if args.action == 'tag':
            make_tag()
        elif args.action == 'build':
            build()
        elif args.action == 'publish':
            publish(args.test)
    except VerboseProcessError as exc:
        print("Error:")
        print(str(exc))
        sys.exit(1)
    except SmokeCheck as exc:
        print(f"Error: {exc}")
        sys.exit(2)


if __name__ == '__main__':
    main()
