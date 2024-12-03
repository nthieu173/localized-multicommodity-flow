let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    pkgs.mdbook
    (pkgs.python311.withPackages (python-pkgs: with python-pkgs; [
      numpy
      matplotlib
      networkx
      scipy
      pip-tools
      black
    ]))
  ];
}
