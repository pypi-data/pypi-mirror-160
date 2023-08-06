"""
Class for starting and stopping named timers.

Here is a simple example. the user and node parameters can be omitted, but they help in case you like
to change the system retrieved values.

from pprint import pprint
from cloudmesh.common.StopWatch import StopWatch

import time

user="gregor"
node="5950x"

for t in ["a", "b"]:
    StopWatch.start(t)
    time.sleep(0.1)
    StopWatch.stop(t)

pprint(StopWatch.get_benchmark(user=user, node=node))

StopWatch.benchmark(user=user, node=node)

## Context Block

StoWatch alos comes with a context block allowing to use the convenient with statement. However thi sis only recommended
when the block is small as it is easy to lose the indentation in larger code. You can also certainly split the code up in
functions so it is easier managable.

Here is a simple example on how to use the with statement, showing that is can be used for streams and files.
The mode tetermins if the file will be recreated, or if it will be appanded on. In addition there is the ability to
write metadata into the record with a dict that can optionally be passed along.

In order not to overwrite the value of an event, you must give it a unique name.

    from cloudmesh.common.StopWatch import StopWatchBlock
    from cloudmesh.common.StopWatch import StopWatch
    from cloudmesh.common.util import readfile

    import time

    data = {"step": "value"}

    StopWatch.event("event-start")
    d = {"key": "value"}
    StopWatch.event("event-with-value", d)

    with StopWatchBlock("total"):
        time.sleep(1.0)

    with StopWatchBlock("dict", data=data):
        time.sleep(1.0)
        data["step"] = 1

    with StopWatchBlock("file", data=data, log="a.log", mode="w"):
        time.sleep(1.0)
        data["step"] = 2

    with StopWatchBlock("append", data=data, log="a.log", mode="a"):
        time.sleep(1.0)
        data["step"] = 3

    content = readfile ("a.log")
    print (79*"=")
    print (content.strip())
    print (79*"=")


    StopWatch.event("event-stop")

    StopWatch.benchmark(sysinfo=False,
                        tag="myexperiment",
                        user="gregor",
                        node="computer",
                        attributes=["timer", "status", "time", "start", "tag", "msg"]

    # for more examples, see our pytest:
    # * <https://github.com/cloudmesh/cloudmesh-common/blob/main/tests/test_stopwatch.py>
    #
    # there we demonstrate how to timers in a loop as individual timers and as sum.
    # We also showcase how to add a message to timers
)

Integration with MLPerf Logging

To also produce output that conforms to MLPerf, cloudmesh. STopWatch will detect if you have mperf logging installed.
We recommend tho install the newest version as follows


::
    git clone https://github.com/mlperf/logging.git mlperf-logging
    pip install -e mlperf-logging

Now you can just use the STopwatch as before.

We will add here aditional information, such as setting up the configuration for mlperf logging

"""
import os
import time
import datetime
import pprint
import yaml
import sys

from cloudmesh.common.console import Console
from cloudmesh.common.Tabulate import Printer
from cloudmesh.common.systeminfo import systeminfo as cm_systeminfo
from cloudmesh.common.util import writefile
from cloudmesh.common.util import readfile
from cloudmesh.common.DateTime import DateTime

from time import perf_counter


def rename(newname):
    """
    decorator to rename a function
    :param newname: function name
    :type newname: str
    :return: renamed function
    :rtype: object
    """

    def decorator(f):
        f.__name__ = newname
        return f

    return decorator


def benchmark(func):
    """
    decorator to benchmark a function
    :param func: function
    :type func: object
    :return: function with benchmarks based on the name of the function
    :rtype: object
    """

    @rename(func.__name__)
    def wrapper(*args, **kwargs):
        StopWatch.start(func.__name__)
        func(*args, **kwargs)
        StopWatch.stop(func.__name__)

    return wrapper


def import_mllog():
    try:
        from mlperf_logging import mllog
    except:  # noqa: E722
        Console.error("You need to install mllogging to use it")
        sys.exit()
    return mllog


class StopWatch(object):
    """
    A class to measure times between events.
    """
    debug = False
    verbose = True
    # Timer start dict
    timer_start = {}
    # Timer end dict
    timer_end = {}
    # Timer diff
    timer_elapsed = {}
    # records a status
    timer_status = {}
    # records a dt
    timer_sum = {}
    # msg
    timer_msg = {}
    # mllogger
    timer_values = {}
    mllogging = False
    mllogger = None

    @classmethod
    def activate_mllog(cls, filename="cloudmesh_mllog.log", config=None):
        # global mllog
        cls._mllog_import = import_mllog()

        if config is None:
            cms_mllog = dict(
                default_namespace="cloudmesh",
                default_stack_offset=1,
                default_clear_line=False
            )
        else:
            cms_mllog = config

        cls.mllogging = True
        cls.mllogger = cls._mllog_import.get_mllogger()
        cls._mllog_import.config(filename=filename)
        cls._mllog_import.config(**cms_mllog
            # useful when refering to linenumbers in separate code
            # root_dir=os.path.normpath(
            #    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", ".."))
        )

    @classmethod
    def progress(cls, percent, status="running", pid=None):
        if pid is None:
            pid = os.getpid()
        if "SLURM_JOB_ID" in os.environ:
            pid = os.environ["SLURM_JOB_ID"] #TODO - may need to be updated (monitor of long running jobs)
        print(f"# cloudmesh status={status} progress={percent} pid={pid}")

    @classmethod
    def progress(cls, percent, status="running", pid=None, variable=None):
        """Prints progress of an event, recording against a pid and providing additional variable.

        :percent: 0-100 value
        :status: Message to associate to the recording, default - running
        :pid: The associated Process ID for this event.
        :variable: Any valid python type with a __str__ method.

        :returns: The progress message as a string
        """
        if pid is None:
            pid = os.getpid()
        if "SLURM_JOB_ID" in os.environ:
            # TODO - may need to be updated (monitor of long running jobs)
            pid = os.environ["SLURM_JOB_ID"]
        msg = f"# cloudmesh status={status} progress={percent} pid={pid}"
        if variable is not None:
            msg = msg + f" variable={variable}"
        print(msg)
        return msg
        try:
            config = yaml.safe_load(readfile(configfile).strip())
        except:  # noqa: E722
            config = {
                "benchmark": {}
            }
        config["benchmark"].update(argv)


    # @classmethod
    # def organization_mllog(cls, configfile, **argv):
    #     mllog = import_mllog()
    #
    #     try:
    #        config = yaml.safe_load(readfile(configfile).strip())
    #     except:
    #         config = {
    #             "benchmark": {}
    #         }
    #     config["benchmark"].update(argv)
    #
    #     for key, attribute in [
    #         (mllog.constants.SUBMISSION_BENCHMARK, 'name'),
    #         (mllog.constants.SUBMISSION_POC_NAME, 'user'),
    #         (mllog.constants.SUBMISSION_POC_EMAIL, 'email'),
    #         (mllog.constants.SUBMISSION_ORG, 'organisation'),
    #         (mllog.constants.SUBMISSION_DIVISION, 'division'),
    #         (mllog.constants.SUBMISSION_STATUS, 'status'),
    #         (mllog.constants.SUBMISSION_PLATFORM, 'platform')
    #         ]:
    #         try:
    #             cls.mllogger.event(key=key, value=config["benchmark"][attribute])
    #         except:
    #             pass

    @classmethod
    def keys(cls):
        """returns the names of the timers"""
        return list(cls.timer_end.keys())

    @classmethod
    def status(cls, name, value):
        """
        starts a timer with the given name.

        :param name: the name of the timer
        :type name: string
        :param value: value of the nameed of a status
        :type value: bool

        """
        if cls.debug:
            print("Timer", name, "status", value)
        cls.timer_status[name] = value

    @classmethod
    def get_message(cls, name):
        """
        starts a timer with the given name.

        :param name: the name of the timer
        :type name: string

        """
        return cls.timer_msg[name]

    @classmethod
    def message(cls, name, value):
        """
        starts a timer with the given name.

        :param name: the name of the timer
        :type name: string
        :param value: the value of the message
        :type value: bool

        """
        cls.timer_msg[name] = value

    @classmethod
    def event(cls, name, msg=None, values=None, suppress_stopwatch=False, suppress_mllog=False):
        """
        Adds an event with a given name, where start and stop is the same time.

        :param name: the name of the timer
        :type name: string
        :param msg: a message to attach to this event
        :type msg: string
        :param values: data that is associated with the event that is converted
                       to a string
        :type values: object
        :param suppress_stopwatch: suppresses executing any stopwatch code.
                                Useful when only logging an mllog event.
        :type suppress_stopwatch: bool
        :param suppress_mllog: suppresses executing any mllog code.  Useful
                               when only interacting with stopwatch timers.
        :type suppress_mllog: bool

        :returns: None
        :rtype: None
        """
        if not suppress_stopwatch:
            StopWatch.start(name, suppress_mllog=True)
            StopWatch.stop(name, suppress_mllog=True)
            StopWatch.timer_end[name] = StopWatch.timer_start[name]
            if values:
                StopWatch.timer_values[name] = values

            if msg is not None:
                StopWatch.message(name, str(msg))
        if cls.mllogging and not suppress_mllog:
            if values is not None:
                cls.mllogger.event(key=name, value=str(values))
            else:
                cls.mllogger.event(key=name)

    @classmethod
    def log_event(cls, **kwargs):
        """Logs an event using the passed keywords as parameters to be logged,
           prefiltered by mlperf_logging's standard api.

        :param kwargs: an unpacked dictionary of key=value entries to be
                       leveraged when logging an event to both the cloudmesh
                       stopwatch and mllog.  If the keyword matches
                       mlperf_logging's constants, the value will be replaced
                       with the standardized string
        :type kwargs: dict
        """
        for key, value in kwargs.items():
            mlkey = cls.mllog_lookup(key)
            cls.event(mlkey, msg=mlkey, values=value)


    @classmethod
    def log_constant(cls, **kwargs):
        """Deprecated.  Use `log_event`."""
        cls.log_event(**kwargs)

    @classmethod
    def mllog_lookup(cls, key: str) -> str:
        """Performs a dynamic lookup for the string representation of a
           mlperf constant.  If the value isn't found, it will return a string
           of the pattern mllog-event-{key}

        :param key: The name of the constant to look up
        :type key: string

        :returns: The decoded value of the constant.
        :rtype: string
        """
        try:
            from mlperf_logging.mllog import constants as mlconst
        except ImportError as e:
            Console.error("You need to install mlperf_logging to use it")
            raise e
        try:
            key_str = getattr(mlconst, key)
        except AttributeError as e:
            key_str = f"mllog-event-{key}"
        return key_str


    @classmethod
    def start(cls, name, values=None, mllog_key=None, suppress_stopwatch=False, suppress_mllog=False):
        """
        starts a timer with the given name.

        :param name: the name of the timer
        :type name: string
        :param values: any python object with a __str__ method to record with
                       the event.
        :type values: object
        :param mllog_key: Specifies the string name of an mllog constant to
                          associate to this timer start.  If no value is passed
                          and mllogging is enabled, then `name` is used.
        :type mllog_key: string
        :param suppress_stopwatch: When true, prevents all traditional
                                   stopwatch logic from running.  This is
                                   useful when attempting to interact with
                                   mllog-only.
        :type suppress_stopwatch: bool
        :param suppress_mllog: When true, prevents all mllog events from
                               executing.  Useful when working with stopwatch
                               timers-only.

        :returns: None
        :rtype: None
        """
        if not suppress_stopwatch:
            if cls.debug:
                print("Timer", name, "started ...")
            if name not in cls.timer_sum:
                cls.timer_sum[name] = 0.0
            cls.timer_start[name] = time.time()
            cls.timer_end[name] = None
            cls.timer_status[name] = None
            cls.timer_msg[name] = None
            if values:
                StopWatch.timer_values[name] = values

        if cls.mllogging and not suppress_mllog:
            if mllog_key is None:
                key = name
            else:
                key = cls.mllog_lookup(mllog_key)
            if values is not None:
                cls.mllogger.start(key=key, value=str(values))
            else:
                cls.mllogger.start(key=key)

    @classmethod
    def stop(cls, name, state=True, values=None, mllog_key=None, suppress_stopwatch=False, suppress_mllog=False):
        """
        stops the timer with a given name.

        :param name: the name of the timer
        :type name: string
        :param state: When true, updates the status of the timer.
        :type state: bool
        :param mllog_key: Specifies the string name of an mllog constant to
                          associate to this timer start.  If no value is passed
                          and mllogging is enabled, then `name` is used.
        :type mllog_key: string
        :param suppress_stopwatch: When true, prevents all traditional
                                   stopwatch logic from running.  This is
                                   useful when attempting to interact with
                                   mllog-only.
        :type suppress_stopwatch: bool
        :param suppress_mllog: When true, prevents all mllog events from
                               executing.  Useful when working with stopwatch
                               timers-only.

        :returns: None
        :rtype: None
        """
        if not suppress_stopwatch:
            cls.timer_end[name] = time.time()
            # if cumulate:
            #    cls.timer_end[name] = cls.timer_end[name] + cls.timer_last[name]
            cls.timer_sum[name] = cls.timer_sum[name] + cls.timer_end[name] - cls.timer_start[name]
            cls.timer_status[name] = state
            if values:
                StopWatch.timer_values[name] = values

        if cls.mllogging and not suppress_mllog:
            if mllog_key is None:
                key = name
            else:
                key = cls.mllog_lookup(mllog_key)
            if values is not None:
                cls.mllogger.end(key=key, value=str(values))
            else:
                cls.mllogger.end(key=key)

        if cls.debug and not suppress_stopwatch:
            print("Timer", name, "stopped ...")

    @classmethod
    def get_status(cls, name):
        """
        sets the status of the timer with a given name.

        :param name: the name of the timer
        :type name: string
        """
        return cls.timer_status[name]

    # noinspection PyPep8
    @classmethod
    def get(cls, name, digits=4):
        """
        returns the time of the timer.

        :param name: the name of the timer
        :type name: string
        :rtype: the elapsed time
        """
        if name in cls.timer_end:
            try:
                diff = cls.timer_end[name] - cls.timer_start[name]
                if round is not None:
                    cls.timer_elapsed[name] = round(diff, digits)
                else:
                    cls.timer_elapsed[name] = diff
                return cls.timer_elapsed[name]
            except:  # noqa: E722
                return None
        else:
            return "undefined"

    @classmethod
    def sum(cls, name, digits=4):
        """
        returns the sum of the timer if used multiple times

        :param name: the name of the timer
        :type name: string
        :rtype: the elapsed time
        """
        if name in cls.timer_end:
            try:
                diff = cls.timer_sum[name]
                if round is not None:
                    return round(diff, digits)
                else:
                    return diff
            except:  # noqa: E722
                return None
        else:
            return "undefined"

    @classmethod
    def clear(cls):
        """
        clear start and end timer_start
        """
        cls.timer_start.clear()
        cls.timer_end.clear()
        cls.timer_sum.clear()
        cls.timer_status.clear()
        cls.timer_elapsed.clear()
        cls.timer_msg.clear()

    @classmethod
    def print(cls, *args):
        """
        prints a timer. The first argument is the label if it exists, the last is the timer
        :param args: label, name
        :return:
        """
        if cls.verbose:
            if len(args) == 2:
                print(args[0], str("{0:.2f}".format(cls.get(args[1]))), "s")
            else:
                raise Exception("StopWatch: wrong number of arguments")

    @classmethod
    def output(cls, name):
        """
        prints a timer. The first argument is the label if it exists, the last is the timer
        :param args: label, name
        :return:
        """
        print(name, str("{0:.2f}".format(cls.get(name))), "s")

    @classmethod
    def __str__(cls):
        """
        returns the string representation of the StopWatch
        :return: string of the StopWatch
        :rtype: str
        """
        s = ""
        for t in cls.timer_end:
            data = {"label": t,
                    "start": str(cls.timer_start[t]),
                    "end": str(cls.timer_end[t]),
                    "status": str(cls.timer_status[t]),
                    "elapsed": str(cls.get(t)),
                    "newline": os.linesep}
            s += "{label} {start} {end} {elapsed} {status} {newline}".format(
                **data)
        return s

    @classmethod
    def systeminfo(cls, data=None):
        """
        Print information about the system

        :param data: additional data to be integrated
        :type data: dict
        :return: a table with data
        :rtype: str
        """
        data_platform = cm_systeminfo()
        if data is not None:
            data_platform.update(data)
        return Printer.attribute(
            data_platform,
            order=["Machine Attribute", "Value"],
            output="table"
        )

    @classmethod
    def get_sysinfo(cls,
                    node=None,
                    user=None):
        data_platform = cm_systeminfo(node=node, user=user)
        return data_platform

    @classmethod
    def get_benchmark(cls,
                      sysinfo=True,
                      tag=None,
                      node=None,
                      user=None,
                      total=False,
                      ):
        """
        prints out all timers in a convenient benchmark table

        :param sysinfo: controls if system info shoul be printed.
        :type sysinfo: bool
        :param csv: contols if the data should be printed also as csv strings
        :type csv: bool
        :param prefix: The prefix used for the csv string
        :type prefix: str
        :param tag: overwrites the tag
        :type tag: str
        :param sum: prints the sums (not used)
        :type sum: bool
        :param node: overwrites the name of the node
        :type node: str
        :param user: overwrites the name of the user
        :type user: str
        :param attributes: list of additional attributes to print
        :type attributes: list
        :return: prints the information
        :rtype: stdout
        """

        #
        # PRINT PLATFORM
        #

        data_platform = cm_systeminfo(user=user, node=node)
        if sysinfo:
            print(Printer.attribute(
                data_platform,
                output="table"
            ))

        benchmark_data = {
            'sysinfo': data_platform,
        }

        #
        # GET TIMERS
        #
        timers = StopWatch.keys()
        total_time = 0.0
        if len(timers) > 0:

            data_timers = {}
            for timer in timers:
                data_timers[timer] = {
                    'start': time.strftime("%Y-%m-%d %H:%M:%S",
                                           time.gmtime(
                                               StopWatch.timer_start[timer])),
                    'stop': time.strftime("%Y-%m-%d %H:%M:%S",
                                          time.gmtime(
                                              StopWatch.timer_end[timer])),
                    'time': StopWatch.get(timer, digits=3),
                    'sum': StopWatch.sum(timer, digits=3),
                    'status': StopWatch.get_status(timer),
                    'msg': StopWatch.get_message(timer),
                    'timer': timer,
                    'tag': tag or ''
                }
                total_time = total_time + StopWatch.get(timer)

            # print(Printer.attribute(data_timers, header=["Command", "Time/s"]))

            if 'benchmark_start_stop' in data_timers:
                del data_timers['benchmark_start_stop']

            for key in data_timers:
                if key != 'benchmark_start_stop' and data_timers[key]['status'] is None:
                    data_timers[key]['status'] = "failed"
                elif data_timers[key]['status'] is not None and data_timers[key]['status']:
                    data_timers[key]['status'] = "ok"

            if total:
                print("Total:", total_time)

            benchmark_data["benchmark"] = data_timers

        else:
            print("ERROR: No timers found")

        return benchmark_data

    @classmethod
    def benchmark(cls,
                  sysinfo=True,
                  timers=True,
                  csv=True,
                  prefix="# csv",
                  tag=None,
                  sum=True,
                  node=None,
                  user=None,
                  attributes=None,
                  total=False,
                  filename=None):
        """
        prints out all timers in a convenient benchmark table

        :param sysinfo: controls if system info shoul be printed.
        :type sysinfo: bool
        :param csv: contols if the data should be printed also as csv strings
        :type csv: bool
        :param prefix: The prefix used for the csv string
        :type prefix: str
        :param tag: overwrites the tag
        :type tag: str
        :param sum: prints the sums (not used)
        :type sum: bool
        :param node: overwrites the name of the node
        :type node: str
        :param user: overwrites the name of the user
        :type user: str
        :param attributes: list of additional attributes to print
        :type attributes: list
        :return: prints the information
        :rtype: stdout
        """

        #
        # PRINT PLATFORM
        #
        content = "\n"

        data_platform = cm_systeminfo(user=user, node=node)
        if sysinfo:
            content = content + Printer.attribute(
                data_platform,
                order=["Machine Attribute", "Value"],
                output="table"
            )
            content = content + "\n"

        if timers:

            #
            # PRINT TIMERS
            #
            timers = StopWatch.keys()
            total_time = 0.0
            if len(timers) > 0:

                data_timers = {}
                for timer in timers:
                    data_timers[timer] = {
                        'start': time.strftime("%Y-%m-%d %H:%M:%S",
                                               time.gmtime(
                                                   StopWatch.timer_start[timer])),
                        'time': StopWatch.get(timer, digits=3),
                        'sum': StopWatch.sum(timer, digits=3),
                        'status': StopWatch.get_status(timer),
                        'msg': StopWatch.get_message(timer),
                        'timer': timer,
                        'tag': tag or ''
                    }
                    try:
                        total_time = total_time + StopWatch.get(timer)
                    except:  # noqa: E722
                        pass
                    for attribute in ["uname.node",
                                      "user",
                                      "uname.system",
                                      "uname.machine",
                                      "platform.version",
                                      "sys.platform"]:
                        if attribute == "user" and user is not None:
                            data_timers[timer][attribute] = user
                        elif attribute == "uname.node" and node is not None:
                            data_timers[timer][attribute] = node
                        else:
                            data_timers[timer][attribute] = data_platform[attribute]

                # print(Printer.attribute(data_timers, header=["Command", "Time/s"]))

                if 'benchmark_start_stop' in data_timers:
                    del data_timers['benchmark_start_stop']

                for key in data_timers:
                    if key != 'benchmark_start_stop' and data_timers[key]['status'] is None:
                        data_timers[key]['status'] = "failed"
                    elif data_timers[key]['status'] is not None and data_timers[key]['status']:
                        data_timers[key]['status'] = "ok"

                if attributes is None:
                    order = [
                        "timer",
                        "status",
                        "time",
                        "sum",
                        "start",
                        "tag",
                        "msg",
                        "uname.node",
                        "user",
                        "uname.system",
                        "platform.version"
                    ]

                    header = [
                        "Name",
                        "Status",
                        "Time",
                        "Sum",
                        "Start",
                        "tag",
                        "msg",
                        "Node",
                        "User",
                        "OS",
                        "Version"
                    ]
                elif attributes == "short":
                    order = [
                        "timer",
                        "status",
                        "time"
                    ]

                    header = [
                        "Name",
                        "Status",
                        "Time"
                    ]
                else:
                    order = attributes
                    header = attributes
                content = content + "\n"
                content = content + Printer.write(
                    data_timers,
                    order=order,
                    header=header,
                    output="table"

                )

                if total:
                    content = content + f"Total: {total_time}"

                content = content + "\n"

                if csv:
                    if prefix is not None:
                        for entry in data_timers:
                            data_timers[entry]["# csv"] = prefix

                        order = ["# csv"] + order

                        content = content + Printer.write(
                            data_timers,
                            order=order,
                            header=header,
                            output="csv"
                        )
                    else:

                        content = content + pprint.pformat(data_timers, indent=4)
                        content = content + "\n"

                        content = content + Printer.write(
                            data_timers,
                            order=order[1:],
                            output="csv"
                        )
                        content = content + "\n"

            else:
                content = content + "ERROR: No timers found\n"

        print(content)
        if filename:
            writefile(filename, content)

    def load(filename,
             label=["name"], label_split_char=" ",
             attributes=['timer',
                         'status',
                         'time',
                         'sum',
                         'start',
                         'tag',
                         'msg',
                         'uname.node',
                         'user',
                         'uname.system',
                         'platform.version']):
        """
        Loads data written to a file from the #csv lines.
        If the timer name has spaces in it, it must also have a label tag in which each lable is the name when
        splitting up the timer name. The list of attributes is the list specified plus the once generated from the
        timer name by splitting.

        Example:
            data = StopWatch.load(logfile, label=["name", "n"], attributes=["timer", "time", "user", "uname.node"])


        :param label:
        :type label:
        :param attributes:
        :type attributes:
        :return:
        :rtype:
        """
        data = []
        headers = []
        content = readfile(logfile)
        lines = Shell.find_lines_with(content, what="# csv")
        data_attributes = lines[0].split(",")
        index_attributes = []
        for attribute in attributes:
            index_attributes.append(data_attributes.index(attribute))
        print(index_attributes)
        headers = attributes + label
        del lines[0]
        for line in lines:
            entry = line.split(",")
            entry = [entry[i] for i in index_attributes]
            label_tags = entry[0].split(label_split_char)
            entry = entry + label_tags
            data.append(entry)

        return {"headers": headers,
                "data": data}


class StopWatchBlock:

    def __init__(self, name, data=None, log=sys.stdout, mode="w"):
        self.name = name
        self.data = data
        self.log = log
        self.is_file = False
        self.start = datetime.datetime.now()
        if type(log) == str:
            self.is_file = True
            self.log = open(log, mode)

    def __enter__(self):
        StopWatch.start(self.name)
        return StopWatch.get(self.name)

    def __exit__(self, type, value, traceback):
        self.stop = datetime.datetime.now()
        StopWatch.stop(self.name)
        entry = StopWatch.get(self.name)
        if self.data:
            print(f"# {self.name}, {entry}, {self.start}, {self.stop}, {self.data}", file=self.log)
        else:
            print(f"# {self.name}, {entry}, {self.start}, {self.stop}", file=self.log)
        if self.is_file:
            self.log.close()
