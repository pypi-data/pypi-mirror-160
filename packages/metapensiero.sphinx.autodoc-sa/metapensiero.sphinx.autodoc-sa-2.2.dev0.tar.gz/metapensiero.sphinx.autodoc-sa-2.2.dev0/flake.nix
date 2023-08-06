# -*- coding: utf-8 -*-
# :Project:   metapensiero.sphinx.autodoc_sa — Development flake
# :Created:   gio 23 giu 2022, 15:33:09
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022 Lele Gaifax
#

{
  description = "metapensiero.sphinx.autodoc_sa development shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        # Current nixpkgs carries Sphinx 4.5 and Docutils 0.18,
        # that are incompatible

        docutils0171 = pkgs.python3Packages.buildPythonPackage rec {
          pname = "docutils";
          version = "0.17.1";
          src = pkgs.python2Packages.fetchPypi {
            inherit pname version;
            hash = "sha256:686577d2e4c32380bb50cbb22f575ed742d58168cee37e99117a854bcd88f125";
          };
          doCheck = false;
        };
      in {
        devShell = pkgs.mkShell {
          name = "Dev shell for mp.sphinx.autodoc_sa";

          packages = [
            docutils0171
          ] ++ (with pkgs; [
            bump2version
            just
            python3
            twine
          ]) ++ (with pkgs.python3Packages; [
            build
            pglast
            pytest
            sphinx
            sqlalchemy
            tomli
          ]);

          shellHook = ''
            export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
          '';
        };
      });
}
