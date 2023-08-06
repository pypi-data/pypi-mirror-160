from datomizer.protos.autodiscoveryservice_pb2 import SchemaDiscoveryDTO, TableDTO, ColumnDTO


class SchemaWrapper(object):
    schema: SchemaDiscoveryDTO

    def __init__(self, schema):
        self.schema = schema

    def tables(self) -> list:
        return self.schema.tables

    def table(self, table_name) -> TableDTO:
        tables = self.tables()
        table: TableDTO
        for table in tables:
            if table_name == table.name:
                return table

        return tables[0]

    def columns(self, table_name) -> list:
        return self.table(table_name).columns

    def column(self, table_name, column_name) -> ColumnDTO:
        columns = self.columns(table_name)
        column: ColumnDTO
        for column in columns:
            if column_name == column.name:
                return column

        return columns[0]

    def __str__(self):
        return str(self.schema)
