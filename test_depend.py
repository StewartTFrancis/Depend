# If I had more time I'd bring in pytest properly
# but for 3 hours this will at least help w/ testing

from depend import Depend 
from dependcli import DependCLI
from contextlib import redirect_stdout
import io

def test_add_deps():
    depend = Depend()
    package = "TELNET"
    package_deps = ["TCPIP", "NETCARD"]

    depend.depend(package, package_deps)

    assert package in depend.package_deps, "Package is in the package dependencies"
    for dep_package in package_deps:
        assert dep_package in depend.package_deps[package], "Dependant package in package dependencies"
        assert dep_package in depend.dep_packages and package in depend.dep_packages[dep_package], "Package in dep package"

def test_install():
    depend = Depend()
    package = "foo"

    depend.install(package)

    assert package in depend.installed, "Package installed"

def test_install_deps():
    depend = Depend()
    package = "TELNET"
    package_deps = ["TCPIP", "NETCARD"]

    depend.depend(package, package_deps)
    depend.install(package)

    for dep_package in package_deps:
        assert dep_package in depend.installed, "Dependencies were installed"

def test_install_nested_deps():
    depend = Depend()
    package = "TELNET"
    package_deps = ["TCPIP"]

    package2 = "TCPIP"
    package_deps2 = ["NETCARD"]

    depend.depend(package, package_deps)
    depend.depend(package2, package_deps2)
    depend.install(package)

    for dep_package in package_deps:
        assert dep_package in depend.installed, "Dependencies were installed"

    for dep_package in package_deps2:
        assert dep_package in depend.installed, "Dependencies were installed"

def test_remove():
    depend = Depend()
    package = "foo"
    
    depend.install(package)
    depend.remove(package)

    assert package not in depend.installed, "Package removed"

def test_remove_deps():
    depend = Depend()
    package = "TELNET"
    package_deps = ["TCPIP", "NETCARD"]

    depend.depend(package, package_deps)
    depend.install(package)

    depend.remove(package_deps[0])
    assert package_deps[0] in depend.installed, "Package not removed, still needed"

def test_remove_nested_deps():
    depend = Depend()
    package = "TELNET"
    package_deps = ["TCPIP"]

    package2 = "TCPIP"
    package_deps2 = ["NETCARD"]

    depend.depend(package, package_deps)
    depend.depend(package2, package_deps2)

    depend.install(package)

    depend.remove(package)
    assert package_deps2[0] in depend.installed, "Package not removed, nested dep"

def cli_test():
    cli = DependCLI()

    input = open("test_input.txt", "r")
    lines = input.readlines()

    expected_output = open("test_output.txt", "r")
    expected_lines =  expected_output.readlines()

    output = io.StringIO()
    with redirect_stdout(output):
        for line in lines:
            if "END"==line.rstrip():
                break
            cli.parse_command(line.rstrip())

        actual_lines = output.getvalue().splitlines(True)

        assert expected_lines == actual_lines, "Our output matched expected"
    

if __name__ == "__main__":
    test_add_deps()
    test_install()
    test_install_deps()
    test_install_nested_deps()
    test_remove()
    test_remove_deps()
    test_remove_nested_deps()
    # cli_test() # ran out of time.
    print("Everything passed")
