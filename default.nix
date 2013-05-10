let
   pkgs = import <nixpkgs> {};
in
{ stdenv ? pkgs.stdenv }:

with pkgs;

stdenv.mkDerivation rec {
  name = "thesis";
 
  src = ./.;
 
  buildInputs = [ texLiveFull haskellngPackages.pandoc ghostscript corefonts liberation_ttf_from_source python ];
 
  configurePhase = ''
    ${python.interpreter} ./waf configure
  '';
 
  buildPhase = ''
    ${python.interpreter} ./waf
  '';
 
  installPhase = ''
    cp -r build/* $out/
  '';
}
