{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell rec {
	buildInputs = with pkgs; [
		yarn nodejs nodePackages.nodemon
	];
}
