# -*- coding: utf-8 -*-
# :Project:   metapensiero.tool.tinject — Development shell
# :Created:   mer 29 giu 2022, 10:40:08
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022 Lele Gaifax
#

{
  description = "metapensiero.tool.tinject";

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

        jinja2-time = pkgs.python3Packages.buildPythonPackage rec {
          pname = "jinja2-time";
          version = "0.2.0";
          src = pkgs.python3Packages.fetchPypi {
            inherit pname version;
            hash = "sha256:d14eaa4d315e7688daa4969f616f226614350c48730bfa1692d2caebd8c90d40";
          };
          propagatedBuildInputs = [
            pkgs.python3Packages.arrow
            pkgs.python3Packages.jinja2
          ];
          doCheck = false;
        };
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = [
              jinja2-time
            ] ++ (with pkgs; [
              bump2version
              just
              python3
              twine
            ]) ++ (with pkgs.python3Packages; [
              build
              questionary
              jinja2
              ruamel-yaml
              tomli
            ]);

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';
          };
        };
      });
}
