{ pkgs }: {
  deps = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.python3Packages.python-telegram-bot
    pkgs.python3Packages.wakeonlan
    pkgs.python3Packages.flask
  ];
}
