"""Class for various platform kex represetntaion.
"""


from typing import Optional


class Kex:
    """Class for various platform kex represetntaion."""

    def __init__(self, kex_name: str, project_name: Optional[str] = None):
        """Kex initializer.

        Arguments:
            project {str} -- project or database name, if None, default is used
            for environments, where project does not make sense, {project} may be used as e.g. database

            kex {str} -- kex name
        """
        if project_name is None:
            from toolkit import current_config

            self.project = current_config.get_storage_manager().project
        else:
            self.project = project_name
        self.project = self.project.replace('"', "")
        self.kex = kex_name.replace('"', "")

    def get_id(self):
        """Get kex id ~ 'project_name.kex_name'

        Returns:
            {str} -- kex id ~ 'project_name.kex_name' or 'database.schema_name'
        """
        dataset_id = "{}.{}".format(self.project, self.kex)
        return dataset_id

    def __str__(self):
        """Stringify kex for nicer outputs"""
        _id = self.get_id() if self.project is not None else self.kex
        return f"<Kex {_id}>"

    def __repr__(self):
        """String representation of Kex object"""
        return str(self)

    def __hash__(self):
        return hash(self.get_id())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.get_id() == other.get_id()

    @staticmethod
    def kex_from_str(kex):
        """Create Kex form string.
         If input argument is not a Kex already, creates Kex from string representing kex id.
         If input is a Kex already, returns original Kex.

        Arguments:
            kex {Kex or str} -- Kex or string ~ either 'project_name.kex_name' or 'kex_name'

        Raises:
            ValueError if kex name is not correctly specified

        Returns:
            {Kex}
        """

        if isinstance(kex, Kex):
            return kex

        elif isinstance(kex, str):
            if len(kex.split(".")) == 1:
                kex_name = kex.split(".")[0]
                return Kex(kex_name)

            elif len(kex.split(".")) == 2:
                project_name = kex.split(".")[0]
                kex_name = kex.split(".")[1]
                return Kex(kex_name, project_name)

            else:
                raise ValueError(
                    "Invalid kex id {}, valid format: either 'project_name.kex_name' or 'kex_name'.".format(kex)
                )
        else:
            raise ValueError("Kex must be either string or Kex, got '{}', which is '{}'.".format(kex, type(kex)))
