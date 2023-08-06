""" Metafile Creator.

    Copyright (c) 2009, 2010, 2011 The PyroScope Project <pyroscope.project@gmail.com>
"""


import hashlib
import logging
import os
import re

from urllib.parse import parse_qs

import bencode

from pyrosimple import config
from pyrosimple.scripts.base import ScriptBase, ScriptBaseWithConfig
from pyrosimple.util import metafile


class MetafileCreator(ScriptBaseWithConfig):
    """
    Create a bittorrent metafile.

    If passed a magnet URL as the only argument, a metafile is created
    in the directory specified via the configuration value 'magnet_watch',
    loadable by rTorrent. Which means you can register 'mktor' as a magnet:
    URL handler in Firefox.
    """

    # argument description for the usage information
    ARGS_HELP = "<dir-or-file> <tracker-url-or-alias>... | <magnet-url>"

    def add_options(self):
        """Add program options."""
        super().add_options()

        self.add_bool_option("-p", "--private", help="disallow DHT and PEX")
        self.add_bool_option("--no-date", help="leave out creation date")
        self.add_value_option(
            "-o",
            "--output-filename",
            "PATH",
            help="optional file name (or target directory) for the metafile",
        )
        self.add_value_option(
            "-r",
            "--root-name",
            "NAME",
            help="optional root name (default is basename of the data path)",
        )
        self.add_value_option(
            "-m",
            "--magnet-watch",
            "NAME",
            help="path to place .meta files from magnet links",
        )
        self.add_value_option(
            "-x",
            "--exclude",
            "PATTERN",
            action="append",
            default=[],
            help="exclude files matching a glob pattern from hashing; can be specified multiple times",
        )
        self.add_value_option(
            "--comment", "TEXT", help="optional human-readable comment"
        )
        self.add_value_option(
            "-s",
            "--set",
            "KEY=VAL",
            action="append",
            default=[],
            help="set a specific key to the given value; omit the '=' to delete a key; can be specified multiple times",
        )
        self.add_bool_option(
            "-H",
            "--hashed",
            "--fast-resume",
            help="create second metafile containing libtorrent fast-resume information",
        )

    # TODO: Optionally pass torrent directly to rTorrent (--load / --start)
    # TODO: Optionally limit disk I/O bandwidth used (incl. a config default!)
    # TODO: Set "encoding" correctly
    # TODO: Support multi-tracker extension ("announce-list" field)
    # TODO: DHT "nodes" field?! [[str IP, int port], ...]
    # TODO: Web-seeding http://www.getright.com/seedtorrent.html
    #       field 'url-list': ['http://...'] on top-level

    def make_magnet_meta(self, magnet_url):
        """Create a magnet-url torrent."""

        if magnet_url.startswith("magnet:"):
            magnet_url = magnet_url[7:]
        meta = {"magnet-url": "magnet:" + magnet_url}
        magnet_params = parse_qs(magnet_url.lstrip("?"))

        meta_name = magnet_params.get("xt", [hashlib.sha1(magnet_url).hexdigest()])[0]
        if "dn" in magnet_params:
            meta_name = f"{magnet_params['dn'][0]}-{meta_name}"
        meta_name = (
            re.sub(r"[^-_,a-zA-Z0-9]+", ".", meta_name)
            .strip(".")
            .replace("urn.btih.", "")
        )

        if not self.options.magnet_watch:
            self.fatal("You MUST set the '--magnet-watch' config option!")
        meta_path = os.path.join(
            self.options.magnet_watch, f"magnet-{meta_name}.torrent"
        )
        self.LOG.debug("Writing magnet-url metafile %r...", meta_path)

        try:
            bencode.bwrite(meta_path, meta)
        except OSError as exc:
            self.fatal("Error writing magnet-url metafile %r (%s)", (meta_path, exc))
            raise

    def mainloop(self):
        """The main loop."""
        if len(self.args) == 1 and "=urn:btih:" in self.args[0]:
            # Handle magnet link
            self.make_magnet_meta(self.args[0])
            return

        if not self.args:
            self.parser.print_help()
            self.parser.exit()
        elif len(self.args) < 2:
            self.parser.error(
                "Expected a path and at least one announce URL, got: %s"
                % (" ".join(self.args),)
            )

        # Create and configure metafile factory
        datapath = self.args[0].rstrip(os.sep)
        metapath = datapath
        if self.options.output_filename:
            metapath = self.options.output_filename
            if os.path.isdir(metapath):
                metapath = os.path.join(metapath, os.path.basename(datapath))
        if not metapath.endswith(".torrent"):
            metapath += ".torrent"
        torrent = metafile.Metafile(metapath)
        torrent.ignore.extend(self.options.exclude)

        def callback(meta):
            "Callback to set label and resume data."
            url_target = meta.get("announce", None) or meta["announce-list"][0]
            meta["info"]["source"] = config.map_announce2alias(url_target)
            meta["info"]["x_cross_seed"] = hashlib.md5(url_target.encode()).hexdigest()
            # Set specific keys?
            metafile.assign_fields(meta, self.options.set)

        # Create and write the metafile(s)
        # TODO: make it work better with multiple trackers (hash only once), also create fast-resume file for each tracker
        meta = torrent.create(
            datapath,
            self.args[1:],
            progress=metafile.console_progress()
            if logging.getLogger().isEnabledFor(logging.WARNING)
            else None,
            root_name=self.options.root_name,
            private=self.options.private,
            no_date=self.options.no_date,
            comment=self.options.comment,
            created_by="PyroSimple",
            callback=callback,
        )

        # Create second metafile with fast-resume?
        if self.options.hashed:
            try:
                metafile.add_fast_resume(meta, datapath)
            except OSError as exc:
                self.fatal(f"Error making fast-resume data ({exc})")
                raise

            hashed_path = re.sub(r"\.torrent$", "", metapath) + "-resume.torrent"
            self.LOG.info("Writing fast-resume metafile %r...", hashed_path)
            try:
                bencode.bwrite(hashed_path, meta)
            except OSError as exc:
                self.fatal(
                    f"Error writing fast-resume metafile {hashed_path!r} ({exc})"
                )
                raise


def run():  # pragma: no cover
    """The entry point."""
    ScriptBase.setup()
    MetafileCreator().run()


if __name__ == "__main__":
    run()
