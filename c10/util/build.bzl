def define_rules(rules):
    rules.package(default_visibility = ["//:__subpackages__"])

    rules.cc_library(
        name = "Array",
        hdrs = ["Array.h"],
        srcs = ["Array.cpp"],
        deps = [":C++17"],
    )

    rules.cc_library(
        name = "C++17",
        hdrs = ["C++17.h"],
        srcs = ["C++17.cpp"],
        deps = ["//c10/macros:Macros"],
    )

    rules.cc_library(
        name = "LeftRight",
        hdrs = ["LeftRight.h"],
        srcs = ["LeftRight.cpp"],
        deps = ["//c10/macros:Macros"],
    )

    rules.cc_library(
        name = "TypeTraits",
        hdrs = ["TypeTraits.h"],
        srcs = ["TypeTraits.cpp"],
        deps = [":C++17"],
    )

    # Temporary targets to export the headers and sources that are not
    # in libraries but are still needed for the //:c10 target that we
    # are slowly replacing.

    rules.filegroup(
        name = "headers",
        srcs = rules.glob(
            ["*.h"],
            exclude=[
                "Array.h",
                "C++17.h",
                "LeftRight.h",
                "TypeTraits.h",
            ]),
        visibility = ["//:__pkg__"],
    )

    rules.filegroup(
        name = "sources",
        srcs = rules.glob(
            ["*.cpp"],
            exclude=[
                "Array.cpp",
                "C++17.cpp",
                "LeftRight.cpp",
                "TypeTraits.cpp",
            ],
        ),
        visibility = ["//:__pkg__"],
    )
