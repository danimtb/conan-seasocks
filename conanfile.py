from conans import ConanFile, CMake, tools
import os, shutil


class SeasocksConan(ConanFile):
    name = "seasocks"
    version = "1.3.2"
    license = "BSD 2-clause \"Simplified\" License"
    url = "https://github.com/Minres/conan-recipes/blob/master/Seasocks"
    description = "Simple, small, C++ embeddable webserver with WebSockets support"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "deflate_support": [True, False]}
    default_options = {"shared": True, "deflate_support": True}
    generators = "cmake"
    exports_sources = "gen_embedded.py"

    def requirements(self):
        if self.options.deflate_support:
            self.requires("zlib/1.2.11@conan/stable")

    def source(self):
        self.run("git clone https://github.com/mattgodbolt/seasocks.git")
        self.run("cd seasocks && git checkout tags/v1.3.2")
        tools.replace_in_file("seasocks/CMakeLists.txt",
                              "project(Seasocks VERSION 1.3.2)",
                              """project(Seasocks VERSION 1.3.2)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")
        tools.replace_in_file("seasocks/CMakeLists.txt",
                              "configure_file(${CMAKE_MODULE_PATH}/Config.h.in",
                              "configure_file(cmake/Config.h.in")
        # tools.replace_in_file("seasocks/CMakeLists.txt",
        #                       "add_compile_options(-Wall -Werror -Wextra -pedantic)",
        #                       "")
        tools.replace_in_file("seasocks/CMakeLists.txt",
                              "PYTHON_BIN python2",
                              "PYTHON_BIN python")
        tools.replace_in_file("seasocks/src/CMakeLists.txt",
                              'add_subdirectory("app/c")',
                              '#add_subdirectory("app/c")')
        shutil.copy2("gen_embedded.py", os.path.join("seasocks", "scripts", "gen_embedded.py"))

    def _cmake_configure(self):
        cmake = CMake(self)
        cmake.definitions["UNITTESTS"] = False
        cmake.configure(source_folder="seasocks")
        return cmake

    def build(self):
        cmake = self._cmake_configure()
        cmake.build()

    def package(self):
        cmake = self._cmake_configure()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["seasocks"]
