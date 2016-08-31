# code-sitter
## Totally ad-hoc continuous integration system for my own needs

Config file should be set as follow:
- config: General information about the project. All entries are mandatory.
    + repo-path: path to the directory containing the hg repo to clone.
    + qemu-path: path where to find an ARM compatible qemu binary.
    + qemu-bin: name of the ARM compatible qemu binary.
    + qemu-args: arguments to give qemu.
    + default-branch: see project's default-branch. If not available, will be
      set to 'default'.


- projects: List of projects to clone and build. Three kinds of projects are
  available.
    + c: they will use the hardcoded recipe for C based projects.
    + smart: they will use the hardcoded recipe for Smart based projects.
    + none: they won't be build directly. Instead they will be reset to the
      'default-branch' and won't be touched anymore.

  Each project is described as follow:
    + name: name of the directory, which should be directly under [repor-path].
    + recipe: "c", "smart" or "none".
    + default-branch: If recipe is set to "none", name of the branch to reset
      the project to. If not available, the selected branch will be
      config:default-branch.
    + branches: List of branches to build. Each branch is described as follow:
      * branch: name of the branch to reset the project to
      * targets: list of platform to build. Each target is described as follow:
        - target: name of the target
        - qemu: boolean attribute whether we should try to run qemu

Author: Vincent Siles

License: MIT

Code Review Tool: Review board version 2.5.6.1
