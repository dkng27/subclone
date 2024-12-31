#!/usr/bin/env python3

import os, argparse, shutil, subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downloads a github repo subdirectory.")
    parser.add_argument(
        "--name",
        type=str,
        help="Rename the directory after cloning",
        dest="name_optional",
    )
    parser.add_argument("-k", "--keep-git", action="store_true", help="Keep the original directory structure after cloning", dest="keep_optional")
    parser.add_argument("url", type=str, help="The URL to process")
    if os.name == 'nt':
        print("\033[93mDue to character restrictions of NTFS sometimes cloning will fail, Linux environment is recommended.\033[0m")

    # Check if git is installed
    if os.system("git --version") != 0:
        raise EnvironmentError("Git is not installed or not found in PATH.")

    args = parser.parse_args()

    url = args.url if args.url else None

    if args.keep_optional and args.name_optional:
        raise ValueError("You can't use both --name and --keep-git at the same time.")

    if url:
        print(f"Processing URL: {url}")
        if "https://github.com" in url and "/tree/" in url:
            parts = url.split("/")
            if len(parts) > 5:
                repo_url = "/".join(parts[:5]) + ".git"
                os.system(
                    f"git clone --no-checkout --depth 1 --sparse -c core.protectNTFS=false --filter=blob:none {repo_url}"
                )           # due to some weird characters, we need to add the core.protectNTFS=false flag so that the clone can be done (sometimes)
                repo_name = parts[4]
                os.chdir(repo_name)
                print(f"Changed directory to: {repo_name}")
                os.system(f"git sparse-checkout init --cone")
                os.system(f'git sparse-checkout add {("/".join(parts[7:] ) + "/")}')
                subprocess.run(["git", "checkout", f"remotes/origin/{parts[6]}"], capture_output=False)
                os.chdir("..")
                if not args.keep_optional:
                    shutil.move(os.path.join(repo_name, *(parts[7:])) + "/", parts[-1] + "/")
                    if os.name == 'nt':
                        shutil.rmtree(repo_name, ignore_errors=True)
                    else:
                        os.system(f"rm -rf {repo_name}")
                if args.name_optional:
                    os.rename(parts[-1], args.name_optional)
                print(f"{parts[-1]} Done Downloading!")
            else:
                raise ValueError("The URL is not a valid GitHub directory.")
        else:
            raise ValueError("The URL is not from GitHub or not a valid directory URL.")
    else:
        raise ValueError("No URL provided.")
