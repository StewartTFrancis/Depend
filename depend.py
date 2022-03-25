"""
    depend.Depend

    This handles our core logic and state.
"""
class Depend():
    def __init__(self):
        # Package dependencies: ex package1 -> package2, package3
        self.package_deps = {}

        # Reverse dep lookup, this speeds up removal by avoiding having 
        # to iterate all packages to see if we"re a dependency 
        self.dep_packages = {}

        # Installed
        self.installed = set()

    def depend(self, package, packages):
        """Registers package dependencies"""
        # If called multiple times we"ll just overwrite with latest
        self.package_deps[package] = packages
        
        for pack in packages:
            if pack not in self.dep_packages:
                # Use a set so we don"t need to worry about duplicates
                self.dep_packages[pack] = set([package])
            else:
                self.dep_packages[pack].add(package)

    def install(self, package):
        """Installs requested package and any dependencies"""
        if package in self.installed:
            print(f"{package} is already installed")
            return
        
        if package in self.package_deps:
            for dep in self.package_deps[package]:
                if dep not in self.installed:
                    self.install(dep)
        
        self.installed.add(package)
        print(f"{package} successfully installed")
    
    def dep_needed(self, package):
        if package in self.dep_packages:
            for dep_package in self.dep_packages[package]:
                if dep_package in self.installed:
                    return True
                else:
                    return False

    def remove(self, package, remove_deps=True):
        """Removes the package and any no longer required dependencies"""
        if package not in self.installed:
            print(f"{package} is not installed")
            return
        
        # check if we"re a dependency of something else installed
        if self.dep_needed(package):
            print(f"{package} is still needed")
            return
        
        # We"re good to remove ourselves
        self.installed.remove(package)
        print(f"{package} successfully removed")

        # Now check our dependencies
        if remove_deps and package in self.package_deps:
            # For each of our dependencies
            for dep in self.package_deps[package]:
                # if it"s still installed, check if it has any dependencies and they are installed
                if dep in self.installed and not self.dep_needed(dep):
                    print(f"{dep} is no longer needed")
                    self.remove(dep, False)

    def list(self):
        print(', '.join(self.installed))
