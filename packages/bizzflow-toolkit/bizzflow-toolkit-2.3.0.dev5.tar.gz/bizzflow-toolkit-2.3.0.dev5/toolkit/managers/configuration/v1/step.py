from typing import Dict

from toolkit.base import Kex
from toolkit.base.step import CopyConf, FilterColumn, FilterConf, UnionConf, WhitelistConf
from toolkit.base.table import Table
from toolkit.managers.configuration.step import BaseStepLoader
from toolkit.managers.configuration.v1.validators import StepValidator



class StepLoader(BaseStepLoader):
    validatorClass = StepValidator

    def _get_unions(self) -> Dict[str, UnionConf]:
        unions = {}
        for table_name, conf in self.step_config["union"].items():
            unions[table_name] = UnionConf(
                tables=[
                    *(
                        Table(
                            table_name=source["table"], kex=Kex(kex_name=source["kex"], project_name=source["project"])
                        )
                        for source in conf["sources"]
                    ),
                    Table.table_from_str(table_name),
                ],
                distinct=conf["distinct"],
            )
        return unions

    def _get_whitelists(self) -> Dict[str, WhitelistConf]:
        whitelists = {}
        for table_name, conf in self.step_config["whitelist"].items():
            whitelists[table_name] = WhitelistConf(columns=conf["columns"])
        return whitelists

    def _get_filters(self) -> Dict[str, FilterConf]:
        filters = {}
        for table_name, conf in self.step_config["filter"].items():
            filters[table_name] = FilterConf(
                custom_query=conf.get("custom_query", ""),
                columns=[
                    FilterColumn(
                        name=column["column"],
                        data_type=column["type"],
                        operator=column["condition"],
                        value=column["value"],
                    )
                    for column in conf.get("columns", [])
                ],
            )
        return filters

    def _get_copies(self) -> Dict[str, CopyConf]:
        copies = {}
        for table_name, conf in self.step_config["copy"].items():
            kex = Kex(kex_name=conf["destination"]["kex"], project_name=conf["destination"]["project"])
            copies[table_name] = CopyConf(
                destination=Table(
                    table_name=conf["destination"]["table"],
                    kex=kex,
                ),
                incremental=conf["incremental"],
                mark_deletes=conf["mark_deletes"],
                primary_keys=conf["primary_key"],
            )
        return copies
