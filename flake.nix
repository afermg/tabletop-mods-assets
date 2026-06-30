{
  description = "Generic stackable-token resource icons for Wingspan TTS mods";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        # The icons derivation: regenerates every SVG from the python
        # source, then rasterizes each to a 256x256 PNG via librsvg.
        # Output layout:
        #   $out/svg/<kind>.svg
        #   $out/png/<kind>.png
        packages.icons = pkgs.stdenv.mkDerivation {
          pname   = "wingspan-resource-icons";
          version = "0.1.0";
          src     = ./.;
          nativeBuildInputs = [ pkgs.python3 pkgs.librsvg ];
          dontUnpack = false;
          buildPhase = ''
            mkdir -p icons
            python3 scripts/gen_resource_icons.py
            mkdir -p $out/svg $out/png
            cp icons/*.svg $out/svg/
            for f in icons/*.svg; do
              name=$(basename "$f" .svg)
              rsvg-convert -w 256 -h 256 "$f" -o "$out/png/$name.png"
            done
          '';
          dontInstall = true;
        };
        packages.default = self.packages.${system}.icons;

        # Dev shell for editing the python generator.
        devShells.default = pkgs.mkShell {
          buildInputs = [ pkgs.python3 pkgs.librsvg ];
        };
      });
}
