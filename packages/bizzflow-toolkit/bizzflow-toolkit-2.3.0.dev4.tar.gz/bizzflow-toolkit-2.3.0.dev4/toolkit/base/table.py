"""Module for various platform table representation.
"""

from toolkit.base.kex import Kex


class TableDetails:
    """Class to store table details."""

    def __init__(
        self,
        created=None,
        description=None,
        location=None,
        modified=None,
        size=None,
        size_readable=None,
        num_rows=None,
        path=None,
        schema=None,
    ):
        """TableDetails initializer.

        Keyword Arguments:
            created {str} -- (default: {None})

            description {str} -- (default: {None})

            location {str} -- (default: {None})

            modified {str} -- (default: {None})

            size {str} -- (default: {None})

            size_readable {str} -- (default: {None})

            num_rows {str} -- (default: {None})

            path {str} -- (default: {None})

            schema {str} -- (default: {None})
        """

        self.created = created
        self.description = description
        self.location = location
        self.modified = modified
        self.size = size
        self.size_readable = size_readable
        self.num_rows = num_rows
        self.path = path
        self.schema = schema

    def to_dict(self):
        """Make dictionary from TableDetails.

        Returns:
            {dict} -- dictionary with table attributes
        """

        return {
            "created": self.created,
            "description": self.description,
            "location:": self.location,
            "modified": self.modified,
            "size": self.size,
            "size_readable": self.size_readable,
            "num_rows": self.num_rows,
            "path": self.path,
            "schema": [{"name": f.name, "mode": f.mode, "type": f.field_type} for f in self.schema],
        }


class TableSchema:
    """Table schema for backends that do not support it natively"""

    def __init__(self, name, field_type, mode=None):
        self.name = name
        self.field_type = field_type
        self.mode = mode


class Table:
    """Class for various platform table representation.

    Raises:
        ValueError: if kex is not specified correctly
    """

    def __init__(self, table_name: str, kex: Kex):
        """Table initializer.

        Arguments:
            table_name {str} -- table name
            kex {Kex} -- Kex
        """

        self.kex = kex
        self.table = table_name
        self.details = None

    def __hash__(self):
        return hash(self.get_full_id())

    def __str__(self):
        return self.full_id

    def __repr__(self):
        return self.full_id

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.get_full_id() == other.get_full_id()

    @property
    def project(self):
        return self.kex.project

    def get_id(self):
        """Get table id ~ 'kex_name.table_name'.

        Returns:
            {str} -- table id ~ 'kex_name.table_name'
        """

        table_id = "{}.{}".format(self.kex.kex, self.table)
        return table_id

    @property
    def full_id(self):
        return self.get_full_id()

    def get_full_id(self):
        """Get table full id ~ 'project_name.kex_name.table_name'.

        Returns:
            {str} -- table id ~ 'project_name.kex_name.table_name'
        """

        table_id = "{}.{}.{}".format(self.project, self.kex.kex, self.table)
        return table_id

    def to_dict(self):
        """Make dictionary from Table.

        Returns:
            {dict} -- representation of Table as dictionary with Table attributes
        """

        return {
            "kex": self.kex.get_id(),
            "name": self.table,
            "project": self.project,
            "id": self.get_full_id(),
            "details": None if self.details is None else self.details.to_dict(),
        }

    @staticmethod
    def table_from_str(table):
        """Create Table from string.
        If input argument is not a Table already, creates Table from string representing table id.
        If input is a Table already, returns original Table.

        Arguments:
            table {Table or str} -- Table or string ~ either 'project_name.kex_name.table_name' or 'kex_name.table_name'

        Raises:
            ValueError if table name is not correctly specified

        Returns:
            {Table}
        """

        if isinstance(table, Table):
            return table

        elif isinstance(table, str):
            if len(table.split(".")) == 2:
                kex_name = table.split(".")[0]
                table_name = table.split(".")[1]
                kex = Kex(kex_name)
                return Table(table_name=table_name, kex=kex)

            elif len(table.split(".")) == 3:
                project_name = table.split(".")[0]
                kex_name = table.split(".")[1]
                table_name = table.split(".")[2]
                kex = Kex(kex_name, project_name)
                return Table(table_name=table_name, kex=kex)

            else:
                raise ValueError(
                    "Invalid table id {}, valid format: either 'project_name.kex_name.table_name' or 'kex_name.table_name'.".format(
                        table
                    )
                )
        else:
            raise ValueError("Table must be either string or Table.")
