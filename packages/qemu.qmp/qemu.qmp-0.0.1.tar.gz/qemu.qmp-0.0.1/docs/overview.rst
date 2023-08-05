Overview
========

.. Normally, I'd use automodule to document the whole file, but we want
   different options for each of the entities that show up on this page,
   so I'm doing it manually. There's a risk of bitrot here.

.. automodule:: qemu.qmp
   :noindex:


Classes
-------

.. Adding the names as header entries is a bit redundant, but it makes
   the HTML sidebar a bit nicer.

QMPClient
~~~~~~~~~

.. Show the methods inherited from Protocol, too.
.. autoclass:: qemu.qmp.QMPClient
   :noindex:
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource


Message
~~~~~~~

.. No need to show the well-known dict methods here.
.. autoclass:: qemu.qmp.Message
   :noindex:
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource


EventListener
~~~~~~~~~~~~~

.. autoclass:: qemu.qmp.EventListener
   :noindex:
   :members:
   :undoc-members:
   :inherited-members:
   :member-order: bysource


Runstate
~~~~~~~~

.. autoclass:: qemu.qmp.Runstate
   :noindex:
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource


Exceptions
----------

.. autoexception:: qemu.qmp.QMPError
   :noindex:
   :members:
   :undoc-members:
   :inherited-members: Exception
   :show-inheritance:
   :member-order: bysource


.. autoexception:: qemu.qmp.StateError
   :noindex:
   :members:
   :undoc-members:
   :inherited-members: Exception
   :show-inheritance:
   :member-order: bysource


.. autoexception:: qemu.qmp.ConnectError
   :noindex:
   :members:
   :undoc-members:
   :inherited-members: Exception
   :show-inheritance:
   :member-order: bysource


.. autoexception:: qemu.qmp.ExecuteError
   :noindex:
   :members:
   :undoc-members:
   :inherited-members: Exception
   :show-inheritance:
   :member-order: bysource


.. autoexception:: qemu.qmp.ExecInterruptedError
   :noindex:
   :members:
   :undoc-members:
   :inherited-members: Exception
   :show-inheritance:
   :member-order: bysource
