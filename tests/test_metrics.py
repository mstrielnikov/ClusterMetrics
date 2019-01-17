import metrics, getpass


def sensors_stat():
    hrdw = metrics.Hardware()
    print(hrdw)

def ram_stat():
    ram = metrics.VirtualMemory()
    print(ram)


def cpu_stat():
    cpu = metrics.Processor()
    print(cpu)


def proc_stat():
    proc = metrics.Prcss()
    print(proc)


def net_stat():
    net = metrics.Network()
    print(net)

def boot_stat():
    boot = metrics.Booting()
    print(boot)


#@debug_test_tools.timer
#@debug_test_tools.check_ram
#@debug_test_tools.check_cpu

metrics.Telemetry().to_do_logs()
