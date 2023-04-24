from subprocess import call, Popen

MODULES = ["path_creator", "signal_functions", "util", "auto_interpretation"]
COMPILER_DIRECTIVES = {'language_level': 3,
                       'cdivision': True,
                       'wraparound': False,
                       'boundscheck': False,
                       'initializedcheck': False,
                       }

for module in MODULES:
    call(
        [
            "cython",
            "-a",
            "-X",
            ",".join(
                f"{key}={val}" for key, val in COMPILER_DIRECTIVES.items()
            ),
            "--cplus",
            "-3",
            f"{module}.pyx",
        ]
    )
    Popen(["firefox", f"{module}.html"])
