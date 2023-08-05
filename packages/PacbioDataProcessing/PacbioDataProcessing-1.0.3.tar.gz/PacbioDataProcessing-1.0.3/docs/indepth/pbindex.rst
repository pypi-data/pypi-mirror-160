.. highlight:: shell

.. _pbindex:

Pbindex
=======

The :ref:`sm-analysis program <sm-analysis>` delegates the indexing of one-molecule
BAM files to ``pbindex``, which must be accessible at runtime.
By default, ``pbindex`` is searched for in the :term:`PATH`. If it is
not found in the :term:`PATH`, you will receive an informative runtime
error message::

  [CRITICAL] [Errno 2] No such file or directory: 'pbindex'

and the :ref:`sm-analysis program <sm-analysis>` itself will stop.

In that case, the instructions in the following sections can help you.


Installing Pbindex
------------------

Probably the easiest way to install ``pbindex`` is with ``conda``.
Have a look at :ref:`setting_up_bioconda`. Once those steps are followed,
and the resulting ``conda`` environment is *active*, install ``pbbam``:

.. prompt:: bash

   conda install -c bioconda pbbam


Upon success, you will be able to pass the path to the ``pbindex``
executable to :ref:`sm-analysis <sm-analysis>` if needed (see below how).


Using Pbindex from `sm-analysis`
--------------------------------

Let us assume that |project| was installed inside a virtual environment
located in::

  /home/dave/.venvs/pdp

and let us assume that ``pbbioconda`` was installed in::

  /home/dave/miniconda3

then, after activating the |project|'s virtual environment:

.. prompt:: bash

   source /home/dave/.venvs/pdp/bin/activate

you can tell ``sm-analysis`` about ``pbindex`` by using a command
line option (:option:`sm-analysis -p`) as follows:

.. prompt:: bash

   sm-analysis --pbindex-path /home/dave/miniconda3/bin/pbindex
