"""
GenericAdder
------------
The `generic_adder` is a processor that adds new fields and values to documents based on a list.
The list can reside inside a rule, inside a file or retrieved from an sql database.


Example
^^^^^^^
..  code-block:: yaml
    :linenos:

    - genericaddername:
        type: generic_adder
        specific_rules:
            - tests/testdata/rules/specific/
        generic_rules:
            - tests/testdata/rules/generic/
        sql_config:
            user: example_user
            password: example_password
            host: "127.0.0.1
            database: example_db
            table: example_table
            target_column: example_column
            add_target_column: True
            timer: 0.1
"""
import re
from logging import Logger
from typing import List, Optional

from attr import define, field, validators

from logprep.abc import Processor
from logprep.processor.generic_adder.mysql_connector import MySQLConnector
from logprep.processor.generic_adder.rule import GenericAdderRule
from logprep.processor.processor_factory_error import InvalidConfigurationError
from logprep.util.helper import get_dotted_field_value


class GenericAdderError(BaseException):
    """Base class for GenericAdder related exceptions."""

    def __init__(self, name: str, message: str):
        super().__init__(f"GenericAdder ({name}): {message}")


class DuplicationError(GenericAdderError):
    """Raise if field already exists."""

    def __init__(self, name: str, skipped_fields: List[str]):
        message = (
            "The following fields already existed and were not overwritten by the GenericAdder: "
        )
        message += " ".join(skipped_fields)

        super().__init__(name, message)


def sql_config_validator(_, attribute, value):
    """validate if a subfield of a dict is valid"""
    if attribute.name == "sql_config" and isinstance(value, dict):
        table = value.get("table")
        if table and re.search(r"\s", table):
            raise InvalidConfigurationError(f"Table in 'sql_config' contains whitespaces!")
        if table and not re.search(r"^[a-zA-Z0-9_]+$", table):
            raise InvalidConfigurationError(
                f"Table in 'sql_config' may only contain alphanumeric characters and underscores!"
            )


class GenericAdder(Processor):
    """Resolve values in documents by referencing a mapping list."""

    @define(kw_only=True)
    class Config(Processor.Config):
        """GenericAdder config"""

        sql_config: Optional[dict] = field(
            default=None,
            validator=[
                validators.optional(validator=validators.instance_of(dict)),
                sql_config_validator,
            ],
        )
        """
        Configuration of the connection to a MySQL database and settings on how to add data from
        the database.
        This field is optional. The database feature will not be used if `sql_config` is omitted.
        Has following subfields:

        - `user` - The user to use when connecting to the MySQL database.
        - `password` - The password to use when connecting to the MySQL database.
        - `host` - The host to use when connecting to the MySQL database.
        - `database` - The database name to use when connecting to the MySQL database.
        - `table` - The table name to use when connecting to the MySQL database.
        - `target_column` - The name of the column whose values are being matched against a value
          from an event.
          If a value matches, the remaining values of the row with the match are being added to
          the event.
        - `add_target_column` - Determines if the target column itself will be added to the event.
          This is set to false per default.
        - `timer` - Period how long to wait (in seconds) before the database table is being checked
          for changes.
          If there is a change, the table is reloaded by Logprep.
        """

    rule_class = GenericAdderRule

    __slots__ = ["_db_connector", "_db_table"]

    _db_table: dict
    """Dict containing table from SQL database"""

    _db_connector: MySQLConnector
    """Connector for MySQL database"""

    def __init__(self, name: str, configuration: Processor.Config, logger: Logger):
        """Initialize a generic adder instance.
        Performs a basic processor initialization. Furthermore, a SQL database and a SQL table are
        being initialized if a SQL configuration exists.
        Parameters
        ----------
        name : str
           Name for the generic adder.
        configuration : Processor.Config
           Configuration for SQL adding and rule loading.
        logger : logging.Logger
           Logger to use.
        """
        super().__init__(name, configuration, logger)

        sql_config = configuration.sql_config
        self._db_connector = MySQLConnector(sql_config, logger) if sql_config else None
        self._db_table = self._db_connector.get_data() if self._db_connector else None

    def _apply_rules(self, event: dict, rule: GenericAdderRule):
        """Apply a matching generic adder rule to the event.
         Add fields and values to the event according to the rules it matches for.
        Additions can come from the rule definition, from a file or from a SQL table.
        The SQL table is initially loaded from the database and then reloaded if it changes.
        At first it checks if a SQL table exists and if it will be used. If it does, it adds all
        values from a matching row in the table to the event. To determine if a row matches, a
        pattern is used on a defined value of the event to extract a subvalue that is then matched
        against a value in a defined column of the SQL table. A dotted path prefix can be applied to
        add the new fields into a shared nested location.
        If no table exists, fields defined withing the rule itself or in a rule file are being added
        to the event.
        Parameters
        ----------
        event : dict
           Name of the event to add keys and values to.
        rule : GenericAdderRule
           A matching generic adder rule.
        Raises
        ------
        DuplicationError
            Raises if an addition would overwrite an existing field or value.
        """

        if self._db_connector and self._db_connector.has_changed():
            self._db_table = self._db_connector.get_data()

        conflicting_fields = []

        use_db = rule.db_target and self._db_table
        items_to_add = [] if use_db else rule.add.items()
        if use_db and rule.db_pattern:
            self._try_adding_from_db(event, items_to_add, rule)

        # Add the items to the event
        for dotted_field, value in items_to_add:
            keys = dotted_field.split(".")
            dict_ = event
            for idx, key in enumerate(keys):
                if key not in dict_:
                    if idx == len(keys) - 1:
                        dict_[key] = value
                        break
                    dict_[key] = {}

                if isinstance(dict_[key], dict):
                    dict_ = dict_[key]
                else:
                    conflicting_fields.append(keys[idx])

        if conflicting_fields:
            raise DuplicationError(self.name, conflicting_fields)

    def _try_adding_from_db(self, event: dict, items_to_add: list, rule: GenericAdderRule):
        """Get the sub part of the value from the event using a regex pattern"""

        value_to_check_in_db = get_dotted_field_value(event, rule.db_target)
        match_with_value_in_db = rule.db_pattern.match(value_to_check_in_db)
        if match_with_value_in_db:
            # Get values to add from db table using the sub part
            value_to_map = match_with_value_in_db.group(1).upper()
            add_from_db = self._db_table.get(value_to_map, [])

            if rule.db_destination_prefix:
                for idx in range(len(add_from_db)):
                    if not add_from_db[idx][0].startswith(rule.db_destination_prefix):
                        add_from_db[idx][0] = f"{rule.db_destination_prefix}.{add_from_db[idx][0]}"

            for item in add_from_db:
                items_to_add.append(item)
