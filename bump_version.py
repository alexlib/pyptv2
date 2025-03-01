#!/usr/bin/env python3
"""Version bumping utility for PyPTV2."""

import argparse
import re
from pathlib import Path

VERSION_FILE = Path('pyptv2/__version__.py')


def read_version():
    """Read the current version from __version__.py."""
    content = VERSION_FILE.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find version string in __version__.py")
    return match.group(1)


def write_version(version):
    """Write a new version to __version__.py."""
    content = VERSION_FILE.read_text()
    content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{version}"',
        content
    )
    VERSION_FILE.write_text(content)


def bump_version(current_version, bump_type):
    """Bump the version according to the specified type."""
    # Parse version components
    if 'dev' in current_version:
        base_version, dev_suffix = current_version.split('dev')
        dev_num = int(dev_suffix) if dev_suffix else 0
        return f"{base_version}dev{dev_num + 1}"
    
    # Parse semantic version
    match = re.match(r'(\d+)\.(\d+)\.(\d+)(.+)?', current_version)
    if not match:
        raise ValueError(f"Invalid version format: {current_version}")
    
    major, minor, patch, suffix = match.groups()
    suffix = suffix or ""
    
    if bump_type == 'major':
        return f"{int(major) + 1}.0.0{suffix}"
    elif bump_type == 'minor':
        return f"{major}.{int(minor) + 1}.0{suffix}"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{int(patch) + 1}{suffix}"
    elif bump_type == 'dev':
        return f"{major}.{minor}.{patch}dev1"
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Bump PyPTV2 version")
    parser.add_argument("--major", action="store_true", help="Bump major version")
    parser.add_argument("--minor", action="store_true", help="Bump minor version")
    parser.add_argument("--patch", action="store_true", help="Bump patch version")
    parser.add_argument("--dev", action="store_true", help="Add/increment dev suffix")
    parser.add_argument("--set", help="Set version to specified value")
    
    args = parser.parse_args()
    
    # Determine bump type
    bump_type = None
    if args.major:
        bump_type = 'major'
    elif args.minor:
        bump_type = 'minor'
    elif args.patch:
        bump_type = 'patch'
    elif args.dev:
        bump_type = 'dev'
    
    if args.set:
        # Set version explicitly
        new_version = args.set
    elif bump_type:
        # Bump version
        current_version = read_version()
        new_version = bump_version(current_version, bump_type)
    else:
        # Just print current version
        current_version = read_version()
        print(f"Current version: {current_version}")
        print("Use --major, --minor, --patch, --dev or --set to bump version")
        return
    
    # Update version
    write_version(new_version)
    print(f"Version updated to: {new_version}")


if __name__ == "__main__":
    main()