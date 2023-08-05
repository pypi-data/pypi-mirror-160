* scal 2.0.0 (2022-07-20)

    * Configuration
      * Configuration files are now using YAML (backward incompatible).
      * Command line options --weeks and --template have been moved to the configuration file.
      * Change default configuration for weeks: display iso numbers, but not work numbers.
    * Templates
      * Fix errors in examples.
      * New template, to generate weekly planners.

    -- Louis Paternault <spalax@gresille.org>

* scal 1.1.0 (2021-08-16)

    * Python support
        * Drop python3.4 to python3.6 support.
        * Add python3.7 to python3.10 support.
    * [core] Get rid of `pkg_resource` module.
    * [feature] Rename .scl option 'lang' by 'language' (but 'lang' is still accepted to preserve backward compatibility).
    * [setup] Replace setup.py by setup.cfg

    -- Louis Paternault <spalax@gresille.org>

* scal 1.0.0 (2018-03-04)

    * Add python3.6 support.
    * Minor code and documentation improvements.

    -- Louis Paternault <spalax@gresille.org>

* scal 0.3.0 (2015-11-27)

    * Can now be called as `python -m scal ARGS`.
    * Generated code is to be compiled with LuaLaTeX (was XeLaTeX before).
    * French examples: Replace "Vacances de Noël" by "Vacances de fin d'année"

    -- Louis Paternault <spalax@gresille.org>

* scal 0.2.1 (2015-06-13)

    * Python3.5 support
    * Minor improvements on generated calendar
    * [doc] Updated French examples
    * Several minor improvements to setup, test and documentation.

    -- Louis Paternault <spalax@gresille.org>

* scal 0.2.0 (2015-03-15)

    * First published version.

    -- Louis Paternault <spalax@gresille.org>
