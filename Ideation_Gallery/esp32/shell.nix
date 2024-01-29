{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
		buildInputs = with pkgs; [
			platformio
			avrdude
			mosquitto
			nodePackages.http-server
		];
}
