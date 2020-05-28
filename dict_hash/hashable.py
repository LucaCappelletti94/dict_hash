class Hashable:
    """The class Hashable has to be implemented by objects you want to hash.

    This abstract class requires the implementation of the method
    consistent_hash, that returns a consistent hash of the function.

    We do NOT want to use the native method __hash__ since that is willfully
    not consistent between python instances, while we want a consistent hash.

    A tipical implementation of the consistent_hash method could be the
    following one:

    ..code::python

        from dict_hash import Hashable, sha256

        class MyObject(Hashable):

            def __init__(self, a:int):
                self._a = a
                self_time = time()

            def consistent_hash(self)->str:
                # The self._time variable here is ignored because we want this
                # object to match also with objects created at other times.
                return sha256({
                    "a":self._a
                })
    """

    def consistent_hash(self) -> str:
        """Return consistent hash of the current object.

        Returns
        ------------------
        A consistent hash of the object.
        """
        raise NotImplementedError(
            "The method consistent_hash must be implemented"
            " by the child classes of Hashable."
        )
