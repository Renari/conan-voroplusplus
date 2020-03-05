from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class VoroPlusPlusConan(ConanFile):
    name = "voro++"
    description = "Voro++ is a open source software library for the computation of the Voronoi diagram."
    topics = ("conan", "voro++", "logging")
    url = "https://github.com/bincrafters/conan-voro++"
    homepage = "http://math.lbl.gov/voro++/"
    license = "BSD Modified"
    generators = "make"

    # Options may need to change depending on the packaged library
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = ()

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            os.unlink('config.mk')
            with open('config.mk', 'w') as f:
                f.write('E_INC=-I../../src\nE_LIB=-L../../src')
            autotools = AutoToolsBuildEnvironment(self)
            autotools.make()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.hh", dst="include", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)
        self.copy(pattern="*.o", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
