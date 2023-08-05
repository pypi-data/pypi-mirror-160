.. highlight:: shell

.. _setting_up_bioconda:

Setting up Bioconda
===================

Probably the easiest (but not the only) way to install some external tools
required by |project|, like :ref:`pbindex`, :ref:`blasr` and :ref:`ccs`,
is through `conda`_. If you decide to follow this route, this section
can hopefully help you.

The complete instructions can be found in `PacBio & Bioconda`_ and the
links therein, but they basically amount to:

1. Install ``conda``. See `installing conda`_ for full details, but it is
   probably enough to use `Miniconda`_, a minimal ``conda`` installer.
   In that case we will assume, as an example, that the ``conda`` environment
   is installed in a directory called::

     /home/dave/miniconda3

   .. warning::

      Depending on the choices made during the process of installing
      ``Miniconda`` you may allow the installer to configure your shell
      such that it *always* activates the ``conda`` environment at login
      time. If that is the case, and you are using :term:`Bash`, you will
      find in your :term:`Bash` initialization file , ``~/.bashrc``, a block
      similar to the following one:

      .. code-block:: console

	 # >>> conda initialize >>>
	 # !! Contents within this block are managed by 'conda init' !!
	 __conda_setup="$('/home/dave/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
	 if [ $? -eq 0 ]; then
             eval "$__conda_setup"
	 else
	     if [ -f "/home/dave/miniconda3/etc/profile.d/conda.sh" ]; then
                 . "/home/dave/miniconda3/etc/profile.d/conda.sh"
	     else
		  export PATH="/home/dave/miniconda3/bin:$PATH"
	     fi
	 fi
	 unset __conda_setup
	 # <<< conda initialize <<<

      Since we are using the ``conda`` environment in a very limited way,
      you can comment that block, prepending a ``#`` to each line.
      
2. Setup the ``channels`` in the ``conda`` environment just created as
   described in `Bioconda`_.


Obviously, for the purpose of having |project| up and running,
it is not necessary to install multiple conda environments to have
:ref:`pbindex`, :ref:`blasr` and :ref:`ccs`. The three tools can be installed in
the same `conda`_ environment.


Once the environment is created, if can be *activated* with:

.. prompt:: bash
	    
   source miniconda3/bin/activate

and *deactivated* with:

.. prompt:: bash

   conda deactivate


.. _`PacBio & Bioconda`: https://github.com/PacificBiosciences/pbbioconda
.. _`Bioconda`: https://bioconda.github.io/#usage
.. _`installing conda`: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
.. _`conda`: https://docs.conda.io
.. _`Miniconda`: https://docs.conda.io/en/latest/miniconda.html
