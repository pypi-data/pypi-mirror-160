# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy — Development shell
# :Created:   ven 24 giu 2022, 11:18:08
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2022 Lele Gaifax
#

{
  description = "metapensiero.sqlalchemy.proxy";

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
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "Dev shell";

            packages = with pkgs; [
              bump2version
              just
              python3
              sphinx
              twine
            ] ++ (with python3.pkgs; [
              build
              sqlalchemy
              tomli
            ]);

            shellHook = ''
               export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
             '';
          };

          testPy39_SA13 =
            let
              py = pkgs.python39;
              sqlalchemy_13 = py.pkgs.buildPythonPackage rec {
                pname = "SQLAlchemy";
                version = "1.3.24";
                src = py.pkgs.fetchPypi {
                  inherit pname version;
                  hash = "sha256:ebbb777cbf9312359b897bf81ba00dae0f5cb69fba2a18265dcc18a6f5ef7519";
                };
                doCheck = false;
              };
            in
              pkgs.mkShell {
                name = "Test Python ${py.version} with SQLAlchemy ${sqlalchemy_13.version}";

                packages = with pkgs; [
                  py
                  py.pkgs.python-rapidjson
                  py.pkgs.pytest
                  py.pkgs.pytest-cov
                  py.pkgs.psycopg2
                  sqlalchemy_13
                ];

                shellHook = ''
                    export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
                  '';
              };

          testPy310_SA14 =
            let
              py = pkgs.python310;
            in
              pkgs.mkShell {
                name = "Test Python ${py.version} with SQLAlchemy ${py.pkgs.sqlalchemy.version}";

                packages = with pkgs; [
                  py
                  py.pkgs.python-rapidjson
                  py.pkgs.pytest
                  py.pkgs.pytest-cov
                  py.pkgs.psycopg2
                  py.pkgs.sqlalchemy
                ];

                shellHook = ''
                    export SQLALCHEMY_WARN_20=1
                    export PYTHONPATH="$(pwd)/src''${PYTHONPATH:+:}$PYTHONPATH"
                  '';
              };
          };

      });
}
