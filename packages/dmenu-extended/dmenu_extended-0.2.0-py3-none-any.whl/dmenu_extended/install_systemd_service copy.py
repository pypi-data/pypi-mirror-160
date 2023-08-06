#!/usr/bin/env python3

import argparse
import grp
import os
import subprocess


def get_executable_path(username):
    executable_name = "dmenu_extended_build_cache"
    executable_paths = ["/usr/local/bin", "/usr/bin", f"/home/{username}/.local/bin"]
    for executable_path in executable_paths:
        path = os.path.join(executable_path, executable_name)
        if os.path.isfile(path):
            return path


def target_files():
    if user_is_root():
        username = os.environ["SUDO_USER"]
    else:
        username = os.environ["USER"]
    groupid = grp.getgrnam(username).gr_gid
    executable_path = get_executable_path(username)
    if not executable_path:
        raise Exception("Could not find dmenu_extended_build_cache executable")

    return {
        "dmenu-extended-update-db.service": "\n".join(
            [
                "[Unit]",
                "Description=Update dmenu-extended cache",
                "Wants=dmenu-extended-update-db.timer",
                "",
                "[Service]",
                "Type=oneshot",
                f"User={username}",
                f"Group={groupid}",
                "ExecStart=" + executable_path,
                "",
                "[Install]",
                "WantedBy=multi-user.target",
                "",
            ]
        ),
        "dmenu-extended-update-db.timer": "\n".join(
            [
                "[Unit]",
                "Description=Run update-dmenu-extended-db.service every 20 minutes",
                "Requires=dmenu-extended-update-db.service",
                "",
                "[Timer]",
                "Unit=dmenu-extended-update-db.service",
                "OnCalendar=*:0/20",
                "",
                "[Install]",
                "WantedBy=timers.target",
                "",
            ]
        ),
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Install dmenu-extended systemd services"
    )
    parser.add_argument("--remove", action="store_true", help="Remove systemd services")
    return parser.parse_args()


def user_is_root():
    return os.geteuid() == 0


def get_install_path():
    if user_is_root():
        # I'm not sure about compatibility between different linux distros
        # so I'm using this path for now until I figure out a better way.
        # It should probably be something like /usr/lib/systemd/system
        return "/etc/systemd/system"
    else:
        return os.path.expanduser("~/.local/share/systemd/user")


def install():
    install_path = get_install_path()
    if not os.path.isdir(install_path):
        print("Creating systemd user directory: " + install_path)
        os.makedirs(install_path)

    for filename, contents in target_files().items():
        path = os.path.join(install_path, filename)
        print("Installing " + filename + " to " + install_path)
        with open(path, "w") as f:
            f.write(contents)


def run_systemd_command(user_command, silent=False):
    command = ["systemctl"]
    if not user_is_root():
        command.append("--user")
    command += user_command
    if silent:
        return (
            subprocess.call(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            == 0
        )
    else:
        return subprocess.call(command) == 0


def remove():
    install_path = get_install_path()
    run_systemd_command(["daemon-reload"])
    for filename in target_files().keys():
        path = os.path.join(install_path, filename)
        if run_systemd_command(["is-enabled", filename], silent=True):
            print("Stopping " + filename + "...")
            run_systemd_command(["stop", filename], silent=True)
            run_systemd_command(["disable", filename], silent=True)
            print("Done")
        if os.path.exists(path):
            print("Removing " + filename + " from " + install_path)
            os.remove(path)
        else:
            print("File " + filename + " does not exist")


def prompt_to_start():
    print("The systemd service has been installed.")
    if input("Do you want to enable it now? [y/N] ").lower() == "y":
        run_systemd_command(["daemon-reload"])
        target = "dmenu-extended-update-db.timer"
        if run_systemd_command(["start", target]) and run_systemd_command(
            ["enable", target]
        ):
            print(f"Started {target}")


def run():
    args = parse_args()
    if args.remove:
        remove()
    else:
        install()
        prompt_to_start()


if __name__ == "__main__":
    run()
