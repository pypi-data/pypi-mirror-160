---
gitea: none
include_toc: true
---
![Build Status](https://drone.mcos.nc/api/badges/laboro/laboro/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

# Laboro

**Laboro** is a **NO-Code / Low-Code** workflow manager that helps you to build and run automated tasks without any coding or system administration skills.

You don't need to know how to install a specific development environment to use **Laboro**.

You don't need to have advanced system administration knowledge to run your **Laboro** automated tasks.

## Development status

**Laboro** is in *beta* stage and is not ready for production yet.

## Status of this documentation

This documentation is an incomplete work in progress and changes may occur frequently until the release of the **Laboro-1.0.0** version.

## Install

**Laboro** leverages the modern container environments such as [*Docker*](https://www.docker.com/) or [*Podman*](https://podman.io/).

The easiest way to install **Laboro** is to install the pre-built and pre-configured container by issuing the following command:

```shell
docker pull mcosystem/laboro:latest
```

That's it !

However, **Laboro** is available through the [*Python Package Index*](https://pypi.org/project/laboro/) for adventurous and expert users willing to simply install **Laboro** on their computer using `pip3 install laboro` and configure it manually.

To get the latest **Laboro** version, run the following command line:

### Install a specific **Laboro** version

The **Laboro** version matches the *Python* **Laboro** package version.

Thus, to install **Laboro** in a specific version, use the corresponding tag:

```bash
docker pull mcosystem/laboro:1.0.0
```

## Running workflows

Once a *workflow* [is configured](#workflow-configuration) and saved in the `/path/to/local/workflowdir`, you can run it by issuing the following command:

Example:
```bash
docker run --name laboro \
            -e TZ=Pacific/Noumea \
            -v /path/to/local/workflowdir:/opt/laboro/workflows:ro \
            -v /path/to/local/workspacesdir:/opt/laboro/workspaces:rw \
            -v /path/to/local/logs:/opt/laboro/log:rw \
            mcosystem/laboro \
            -w workflow_demo_1 workflow_demo_2 workflow_demo_3
```

In this example the 3 workflows` workflow_demo_1`,` workflow_demo_2`,` workflow_demo_3` will be run sequentially in the specified order within a container which time zone is set to `Pacific/Noumea`. The container also has three host directories mounted:
- `/path/to/local/workflowdir` mounted on `/opt/laboro/workflows`
- `/path/to/local/workspacesdir` mounted on `/opt/laboro/workspaces`
- `/path/to/local/logs` mounted on `/opt/laboro/log`


Example of a **Laboro** container running a workflow named `workflow_demo` (slow motion) :
![Laboro demonstration](./media/demo.svg)


## Modules

**Laboro** capabilities are extended through *modules* delivered as *Python* packages.

### Available Modules

Not documented yet.

### Code your own module

Not documented yet.

#### Write the module specification

Not documented yet.

## Concepts


**Laboro** lays on 5 fundamental concepts: [*workflow*](#workflow), [*packages*](#package), [*steps*](#step), [*actions*](#action), [*method*](#method).

Each of these concepts are described in technical details in the [*configuration section*](#configuration).

### Workflow

A **workflow** is a set of [*packages*](#package) and [*steps*](#step). Basically it is the container that embed all the tasks needed that you want to achieve by running it.

#### Package

A **package** is a package in the way *Python*, the programming language underlying **Laboro**, call the deliverable set of code that can be installed.

**Laboro** itself is a *Python* package.

#### Step

A **step** is a set of [*actions*](#action). It describes all actions in that set and the condition in which they will be executed.

#### Action

**Laboro** relies on the **Python** programming language which is an *object oriented programming language*.

This type of languages propose some abstract representation called *objects* that have some *properties* and *methods*.

An object configured with specific parameters is called an *instance* and by calling the *methods* of an instance, you can execute the code that resides inside these methods.

An **action** is the description of an *instance*, its parameters and the condition in which its method will be be executed.

More on that in the [*workflow configuration section*](#workflow-configuration).

#### Method

As seen in the above [*Action section*](#action), a *method* is a description of an *object method*, its parameters and the condition in which it will be be executed.


## Configuration

All aspects of **Laboro**, its main configuration as the workflow configuration are managed through *YAML* configuration files.

### Main configuration

The default global configuration file is `/etc/laboro/laboro.yml`. This file is provided by the **Laboro** container image and should not be modified.

However, this file is auto-generated **at build time** from the parameters given to container build command. Passing parameters at build time ascertains that all needed directories are created with the expected permissions (See the [container/README.md](./container/README.md) for further details on the available configuration parameters and how to build a custom **Laboro** container image).

Even if **Laboro** is a container based application, modification of the default global configuration file outside build time (i.e. by mounting a container volume at run time) is not expected nor supported.

If you choose to do so, please, don't forget to create the directories according to your configuration file and apply the right permissions to them.

Example of global configuration file:
```YAML
---
laboro:
  histdir: /opt/laboro/log/hist
  workspacedir: /opt/laboro/workspaces
  workflowdir:  /opt/laboro/workflows
  log:
    dir:  /opt/laboro/log
    level: INFO
```

### Workflow configuration

A *workflow* is described by a *YAML* configuration file. Each workflow configuration file must be in the `laboro.workflowdir` directory specified in the [main configuration file](#main-configuration).

*TL;DR*: A complete working workflow configuration is [available in the test suite](./tests/files/workflow_demo.yml).

A *workflow* has the following properties:

- `name`: The name of the workflow. A simple string identifying your workflow
- `packages`: A list of *Python* packages that should be installed before running the workflow. All python packages listed here will be installed prior to workflow execution.
To prevent abusive and hazardous package installation, each package name **must** match the following regular expression `^laboro_.*`.
- `workspace`: A section which has a unique key `delete_on_exit` that accepts a boolean value. If set to `True`, the [workspace](#workspace) will be deleted at the end of the workflow.
- `steps`: A list of [*step*](#step-1). Steps will be executed sequentially in the specified order.


Example:

```YAML
---
name: Demo workflow
packages:
  - laboro_demo
workspace:
  delete_on_exit: True
steps:
  - ...
```

In this example the *Python* package `laboro_demo` will be installed prior to the execution of the workflow named `Demo workflow`. When the workflow end, the workspace associated with it and all its content will be deleted.

#### Step

A step has the following properties:

- `name`: The name of the step. A string that **should** be unique in the steps list.
- `loop`: Optional. The description of an iterable object (a list or a dictionary) on which the step will be repeated. If no `loop` property is defined, the step will be executed only once. See the (*Loops* section)(#loops) for further details on loops.
- `when`: Optional. The string representation of an expression that **must** evaluates as a boolean. The result of the evaluation of this expression will be used as a condition to the step execution. See the (*Conditional execution* section)(#conditional-execution) for further details on conditional executions.
- `actions`: A list of [*action*](#action-1). Actions will be executed sequentially in the specified order.

Example:

```YAML
name: Step 1
loop:
  - Nobody
  - expects
  - 'the Spanish Inquisition !'
  - spam
  - spam
  - spam
when: "$step_item$ != 'spam'"
actions:
  - ...
```

In this example the step named `Step 1` will loop over all values declared in its loop property and will be executed only when the [**step loop variable**](#loops) `$step_item$` will have any value different than `spam`.

See [the variables section](#variables) for further details on how to use variables.

#### Action

An *action* has the following properties:

- `name`: A string specifying the name of the action. This name **should** be unique in the workflow.
- `loop`: Optional. The description of an iterable object (a list or a dictionary) on which the acton will be repeated. If no `loop` property is defined, the action will be executed only once. See the (*Loops* section)(#loops) for further details on loops.
- `when`: Optional. The string representation of an expression that **must** evaluates as a boolean. The result of the evaluation of this expression will be used as a condition to the action execution. See the (*Conditional execution* section)(#conditional-execution) for further details on conditional executions.
- `instance`: the description of the [*instance*](#instance)

Example:

```YAML
name: Action 1
when: '$step_item$ != "spam"'
instance:
  ...
```
In this example the action named `Action 1` will be executed when the [**step loop variable**](#loops) `$step_item$` will have any other value than `spam`.

See [the variables section](#variables) for further details on how to use variables.

#### Instance

An *instance* describes how an object will be instantiated. It has the following properties:

- `name`: A string specifying the name of the instance. This name **should** be unique in the workflow and will be used as the variable name in which the *instance* will be stored. Multiple instance declaration with the same name property will override each other and the last declared within the execution scope will be kept.
- `module`: The *Python* module in which the object *class* can be found. This module must be available (see [*packages*](#workflow-configuration)) will be imported.
- `class`: A string specifying the *class* of the object to be instantiated. The specified class **must** be part of the specified *module*.
- `args`: Optional. A dictionary representation of the arguments that will be used for the object instantiation. This dictionary **must** use the expected argument names as keys, and the argument values as value. The `args` property can be omitted if no argument is necessary to the method call.
- `instantiate`: A boolean. If set to `True`, the object will be instantiated and the instance stored in the variable named after the `name` property. If set to `False`, the object will not be instantiated and all methods will be called upon the the object previously stored in the variable named after the `name` property. This allow instance reutilization across steps or actions.
- `methods`: A list of all methods that should be executed. Methods will be executed sequentially in the specified order.

Example:

```YAML
instance:
  name: my_demo
  module: laboro_demo
  class: Demo
  args:
    is_demo: True
    name: Demo Class
    password: p455w0rD_01
    list_only: True
    demo_list:
      - Laboro
      - Rocks
  instantiate: True
  methods:
    - ...
```

In this example, the module name `laboro_demo` will be imported, an object of the class `laboro_demo.Demo` will be instantiated withe the arguments `is_demo`, `name`, `password`, `list_only` and `demo_list`. The resulting instance will be stored in a variable called `my_demo`.

See [the variables section](#variables) for further details on how to use variables.

#### Method

A *method* has the following properties:

- `name`: A string specifying the method name. This name **must** be the method name as declared in the *instance* object class source code.
- `loop`: Optional. The description of an iterable object (a list or a dictionary) on which the method will be repeated. If no `loop` property is defined, the method will be executed only once. See the (*Loops* section)(#loops) for further details on loops.
- `when`: Optional. The string representation of an expression that **must** evaluates as a boolean. The result of the evaluation of this expression will be used as a condition to the method execution. See the (*Conditional execution* section)(#conditional-execution) for further details on conditional executions.
- `args`: Optional. A dictionary representation of the arguments that will be passed to the method. This dictionary **must** use the expected argument names as keys, and the argument values as value. The `args` property can be omitted if no argument is necessary to the method call.
- `output`: A string specifying a variable name in which the return value of the method will be stored. If no output property is specified the return value of the method will be lost.

Example:

```YAML
name: get_title
loop: $store$books
when: $method_item$['author'] == "Plato"
args:
  title: $method_item$
output: book_title
```

In this example the method `get_title` will be executed for each item stored in the `books` variable and when *method loop variable* `author` item value is "*Plato*".
The argument name passed to the method is `title` and its value is the value of the  *method loop variable*.

The value returned by the `get_title` method will be stored in a variable named `book_title`.

See [the variables section](#variables) for further details on how to use variables.


## Variables

By using their `output` property, **Laboro** can store values returned by [*methods*](#method-1).

Once stored, a variable is available on **the whole workflow scope** and can be used in any subsequent property including `loop` and `when` properties).

Calling a variable in a loop is done by prefixing its name by `$store$`.

Example:

```YAML
methods:
  - name: get_books
    output: books
  - name: get_title
    loop: $store$books
    when: $method_item$['author'] == "Plato"
    args:
      title: $method_item$
    output: book_title
```

In this example the return value of the `get_books` method is stored in the `books` variable and then used:
- As a `get_title` [*method loop iterable*](#loops).
- As part of the execution condition of the method `get_title`.

## Files

Values returned by methods can also be stored in file using the ``$file$`` prefix. The file will be placed within the [workspace](#workspaces) and be named as the specified variable name.

Calling the filename back and pass it as an argument to a method is also done with the ``$file$`` prefix.


Example:

```YAML
methods:
  - name: get_books
    output: $file$books.txt
  - name: get_titles
    args:
      bookfile: $file$books.txt
```

In this example the return value of the `get_books` method is stored in a file named `books.txt`.
The file name is then used as the `bookfile` argument of the `get_titles` method.

**Note**: When called back, a ``$file$`` prefixed variable will only return the **full file name path** of the specified file. It's up to the method to open and make needed operations on the file.


## Datafiles

Similarly to the ``$file$`` prefix, the ``$datafile`` prefix is used to provide files access to methods. Those `data files` are presistent across workflow sessions and **are never deleted** after workflow execution. They are usually used as static data files such as template files.

Values returned by methods can also be stored in file using the ``$datafile$`` prefix. The file will be placed within the [workspace](#workspaces) main directory and be named as the specified variable name.

Calling the filename back and pass it as an argument to a method is also done with the ``$datafile$`` prefix.

Users may provide `data files` through a host directory mounted as a container volume on the ``${LABORO_WORKSPACEDIR}`` (See [example](#running-workflows)).

Example:

```YAML
methods:
  - name: get_book_data
      title: Redgauntlet
      author: Sir Walter Scott
    output: $store$book_data
  - name: gen_title_label
    args:
      data: $store$book_data
      template: $datafile$book_label.template
```

In this example the return value of the `get_book_data` method is stored in a variable named `book_data`.
The `book_data` variable is the used as an argument of `gen_title_label` method.
The file name is then used as the `bookfile` argument of the `get_titles` method.
A `template` argument is also passed to the `get_titles` method as a `datafile`. The ``book_label.template`` will be searched within the [main workspace directory of the workflow](#workspaces).

**Note**: When called back, a ``$datafile$`` prefixed variable will only return the **full file name path** of the specified file. It's up to the method to open and make needed operations on the file.


## Loops

*Steps*, *actions* and *method* have a `loop` property that accepts any *iterable* object as a value.

When the `loop` property is set, a specific variable will store each item in the *iterable* object for each execution.

The specific variable name depends on the object the `loop` property is set:

| Object | Loop variable | Call syntax     |
| ------ | ------------- | --------------- |
| Step   | `step_item`   | `$step_item$`   |
| Action | `action_item` | `$action_item$` |
| Method | `method_item` | `$method_item$` |

Once stored, a loop variable is available **for all objects within and beneath its declaration level** and can be used in any subsequent property including `loop` and `when` properties).

Example:

```YAML
steps:
  - name: Step 1
    loop:
      - item1: Nobody
        item2: expects
        item3: 'the Spanish Inquisition !'
      - item1: spam
        item2: spam
        item3: spam
    actions:
      - name: Action 1
        when: '$step_item$["item3"] != "spam"'
        instance:
          name: my_instance
          module: laboro_fake.submodule
          class: FakeObject
          instantiate: True
          methods:
            - name: get_arg_value
              args:
                argument: $step_item$
```

In this example, a list containing two dictionaries is declared as a *step loop iterable*.
When the step is executed, the step variable `step_item` will get the value of each of the dictionary making it available for all actions is the step.

## Workflow sessions

Each execution of a specific workflow is identified by a unique identifier called a `session`. The `session` identifier is a string representation of an [`uuid.uuid4`](https://docs.python.org/3/library/uuid.html?highlight=uuid#uuid.uuid4) object. This session identifier is stored in the [workflow execution history file](#execution-history).

The [workflow log file](#logging) and the [session `workspace`](#workspaces) are named after this property.

## Execution history

Each workflow has its own history database situated in the `laboro.histdir` directory in which each [workflow execution session](#workflows-session) parameters are stored

The default `laboro.histdir` value is `/opt/laboro/log/hist`.

This history database is a *sqlite3* database named after the [workflow `name` property](#workflow-configuration).

For each workflow execution the following data are stored:
- The workflow name
- The [workflow session id](#workflows-sessions)
- The workflow start date as a timestamp
- The workflow end date as a timestamp
- The workflow execution time in a human readable format
- The workflow parameters as a dictionary representation
- The exit code: 0 if exited without error, a detailed error message otherwise.

## Workspaces

Each [workflow](#workflows) has a file storage space named after [the workflow `name` property](#workflow-configuration) and situated under the `laboro.workspacedir` directory. This directory is called the `main workspace directory`.

Some **Laboro** modules such as the ``laboro-template`` module may need user provided `data files` used for each execution of the workflow. Such `data files` are searched in the `main workspace directory`.

For each workflow execution a sub-directory named after the [workflow session id](#workflow-sessions) is created under the `main workspace directory` at runtime. Any [**Laboro** modules](#modules) can use this `workspace` to store file for later use within the workflow. This directory is called the `session workspace directory`.

For further details on file storage, see [the `files` section](#files) and [the `datafiles` section](#datafiles)

**Note*:*
- When the [`workspace.delete_on_exit` workflow property](#workspace) is set to `True`, the `session workspace directory` and its content is deleted at the end of the workflow execution even when the workflow exit on error.
- The `main workspace directory` is never deleted even if the `workspace.delete_on_exit` workflow property is set to ``True``.

```
-+- workspacedir/
      |
      +- my_workflow_1/
      |    |
      |    +- data_file_1
      |    |
      |    +- workflow_1_session_1/
      |    |    |
      |    |    + file_1
      |    |
      |    +- workflow_1_session_2/
      |         |
      |         + file_1
      |
      +- my_workflow_2/
           |
           +- data_file_1
           |
           +- workflow_2_session_1/
           |    |
           |    + file_1
           |
           +- workflow_ 2_session_2/

```

## Logging

**Laboro** logging configuration is set from the [main **laboro** configuration file](#main-configuration).

The default container configuration set the "${LABORO_LOGDIR}" variable to ``/var/log/laboro`` so the log directory can be easily mounted at runtime from the host with the following command:

```bash
docker run --name laboro \
           -e TZ=Pacific/Noumea \
           -v /path/to/local/workflowdir:/opt/laboro/workflows:ro \
           -v /path/to/local/logdir:/var/log/laboro:rw \
           mcosystem/laboro \
           -w my_workflow_1 my_workflow_2
```

All workflows logs are stored in the ``laboro.log.dir`` directory and each [workflow](#workflows) has a specific directory where its session logs will be stored.

```
-+- logdir/
     |
     +- my_workflow_1/
     |    |
     |    +- workflow_1_session_1.log
     |    |
     |    +- workflow_1_session_2.log
     |
       +- my_workflow_2/
            |
            +- workflow_2_session_1.log
```

### Log levels

Log level is a [workflow configuration](#main-configuration) and must be set to one of the following values:

| Log levels   |
| ------------ |
| `DEBUG`      |
| `INFO`       |
| `WARNING`    |
| `ERROR`      |
| `CRITICAL`   |


### Secrets management

Not documented yet.

### Log date and time

The default time zone of the **Laboro** container image is `UTC`.

This can be changed by setting the desired time zone setting by using the `TZ` environment variable to the container.

Example:
```shell
docker run --name laboro \
            -e TZ=Pacific/Noumea \
            -v /path/to/local/workflowdir:/opt/laboro/workflows:ro \
            -v /path/to/local/logs:/opt/laboro/log:rw \
            mcosystem/laboro \
            -w workflow_demo
```

