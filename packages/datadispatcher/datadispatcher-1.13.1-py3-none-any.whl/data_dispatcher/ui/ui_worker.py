import sys, time
from .ui_lib import to_did, from_did, pretty_json, print_handles
from .cli import CLI, CLICommand, InvalidOptions, InvalidArguments
from data_dispatcher.api import NotFoundError

class NextFileCommand(CLICommand):
    
    Opts = "jt:c:w:"
    MinArgs = 1
    Usage = """[options] <project_id> -- get next available file
             -w <worker id>     -- specify worker id
             -c <cpu site>      -- choose the file according to the CPU/RSE proximity map for the CPU site
             -j                 -- as JSON
             -t <timeout>       -- wait for next file until "timeout" seconds, 
                                   otherwise, wait until the project finishes
    """

    def __call__(self, command, client, opts, args):
        project_id = int(args[0])
        worker_id = opts.get("-w")
        as_json = "-j" in opts
        timeout = opts.get("-t")
        if timeout is not None: timeout = int(timeout)
        cpu_site = opts.get("-c")
        done = False
        t0 = time.time()
        t1 = None if timeout is None else t0 + timeout
        retry = True
        while retry:
            try:    
                project_info = client.get_project(project_id)
                if not project_info["active"]:
                    print("done")
                    sys.exit(1)    # project finished
                reply = client.next_file(project_id, cpu_site, worker_id=worker_id)
                info = reply["handle"]
                reason = reply["reason"]
                retry = reply["retry"]
            except NotFoundError:
                print("project not found")
                sys.exit(1)
            if info:
                if as_json:
                    info["replicas"] = sorted(info["replicas"].values(), key=lambda r: -r["preference"])
                    print(pretty_json(info))
                else:
                    print("%s:%s" % (info["namespace"], info["name"]))
                sys.exit(0)
            if retry:
                if timeout is None or (timeout > 0 and time.time() < t1):
                    dt = 5
                    if t1 is not None:
                        dt = min(5, t1-time.time())
                    if dt > 0:
                        time.sleep(dt)
                else:
                    print("timeout")
                    sys.exit(1)        # timeout
           

class DoneCommand(CLICommand):
    
    MinArgs = 2
    Usage = """<project id> <DID>                               -- mark the file as done"""
    
    def __call__(self, command, client, opts, args):
        project_id, did = args
        client.file_done(int(project_id), did)
    
class FailedCommand(CLICommand):
    
    Opts = "f"
    MinArgs = 2
    Usage = """[-f] <project id> <DID>                          -- mark the file as failed
        -f            -- final, do not retry the file
    """
    
    def __call__(self, command, client, opts, args):
        project_id, did = args
        client.file_failed(int(project_id), did, retry = not "-f" in opts)


class IDCommand(CLICommand):
    
    Opts = "n"
    Usage = """[-n|<worker id>]                                 -- set or print worker id
        -n          -- generate random worker id
        
        worker id will be saved in <CWD>/.worker_id
    """
    
    def __call__(self, command, client, opts, args):
        if "-n" in opts:
            worker_id = client.new_worker_id()
        elif args:
            worker_id = args[0]
            client.new_worker_id(worker_id)
        else:
            worker_id = client.WorkerID
        if not worker_id:
            print("worker id unknown")
            sys.exit(1)
        print(worker_id)

WorkerCLI = CLI(
    "id",       IDCommand(),
    "next",     NextFileCommand(),
    "done",     DoneCommand(),
    "failed",   FailedCommand()
)
