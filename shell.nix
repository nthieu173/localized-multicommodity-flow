let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python311.withPackages (python-pkgs: with python-pkgs; [
      pip-tools
      numpy
      pettingzoo
      pydantic
      black
    ]))
  ];
}
