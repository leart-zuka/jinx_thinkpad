# Drop next to config.h, Doodlebomb.ttf, jinxbar and jinxbar-dwm.diff,
# then add ./jinx.nix to `imports` in configuration.nix.
{ pkgs, ... }:
let
  doodlebomb = pkgs.runCommand "doodlebomb-font" { } ''
    install -Dm644 ${./Doodlebomb.ttf} $out/share/fonts/truetype/Doodlebomb.ttf
  '';
  jinxbar = pkgs.writeShellApplication {
    name = "jinxbar";
    runtimeInputs = [ pkgs.xorg.xsetroot pkgs.xorg.xwininfo pkgs.coreutils ];
    text = builtins.readFile ./jinxbar;
    checkPhase = "";            # skip shellcheck on the colour escapes
  };
in {
  fonts.packages = [ doodlebomb ];

  # prompt: copy starship.toml to ~/.config/starship.toml
  # (the NixOS module leaves a user file in place when one exists)
  programs.starship.enable = true;
  environment.systemPackages = [ jinxbar pkgs.feh ];

  # nixpkgs' dwm takes `conf` (your config.h) and `patches` directly
  services.xserver.windowManager.dwm.package = pkgs.dwm.override {
    conf = ./config.h;
    patches = [
      ./jinxbar-dwm.diff                  # 3-zone bar + colour/rect escapes (replaces status2d)
      # ./dwm-vanitygaps-6.4.diff         # gaps + fibonacci layouts: uncomment, and see
                                          # config.vanitygaps.h (applied after jinxbar's patch)
    ];
  };
}
