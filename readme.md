# Distributed build service experiment

**NOTE**: this program is insecure. Do not ever run in except for
  testing and in closed private networks. There may be bugs and data
  loss. Only use virtual machines or containers.

## The quick setup

You need:

 - an shared disk
 - a "master server" machine or container
 - one or more worker machines or containers
 - a "user desktop" machine

Mount the shared drive in the same path on all builder
machines/containers and the user desktop.

Make sure all builders are identical.

Start `masterservice.py` on the coordinator machine.

Start `workerservice.py master_host_address` on all workers.

Go to desktop machine and run this:

    FORCE_LOCAL=1 \
    CC='/path/to/cwrapper.py master_hostname gcc' \
    CXX='/path/to/cwrapper.py master_hostname g++' \
    meson/cmake/configure/etc <other options>

Where `master_hostname` is the name or IP address of the machine
running the master server process. This sets up the system. To do the
compilation do:

    make/ninja/etc -j total_number_of_cores

So if you have 3 machines with 4 cores each, you'd use `-j 12`.

