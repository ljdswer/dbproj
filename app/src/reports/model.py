from os import path
from flask import current_app
from ..db import SQLProvider, select, DataError
from dataclasses import dataclass
from typing import Union, List, Dict

module_path = path.dirname(path.abspath(__file__))
sql_provider = SQLProvider(path.join(module_path, "sql"))


@dataclass
class Result:
    value: Union[Dict, None] = None
    error: str = ""

    def is_err(self):
        return bool(self.error)

    def is_ok(self):
        return not self.is_err()


def get_report_config(report_type: str) -> Result:
    report_config = current_app.config['REPORTS'].get(report_type)
    if not report_config:
        return Result(error="Некорректный тип отчета")    
    return Result(value=report_config)

def create_report(report_type: str, form_data) -> Result:
    report_config_result = get_report_config(report_type)
    if report_config_result.is_err():
        return report_config_result

    fields = report_config_result.value['fields']
    field_values = [form_data.get(field['field_name']) for field in fields]
    if any(not value for value in field_values):
        return Result(error="Все поля должны быть заполнены")

    sql = sql_provider.get(report_config_result.value["sql_create"])
    try:
        result = select(current_app.config["DATABASE"]["reports"], sql, field_values)
    except DataError:
        return Result(error="Запрос некорректен")
    
    status = result[0].get('Status')
    if status == "ALREADYEXISTS":
        return Result(error="Этот отчёт уже был создан")
    elif status == "NODATA":
        return Result(error="Нет данных для включения в отчёт")

    return Result(value=result)


def view_report(report_type: str, form_data) -> Result:
    report_config_result = get_report_config(report_type)
    if report_config_result.is_err():
        return report_config_result

    fields = report_config_result.value['fields']
    field_values = [form_data.get(field['field_name']) for field in fields]
    if any(not value for value in field_values):
        return Result(error="Все поля должны быть заполнены")

    sql = sql_provider.get(report_config_result.value["sql_view"])
    try:
        result = select(current_app.config["DATABASE"]["reports"], sql, field_values)
    except DataError:
        return Result(error="Запрос некорректен")
    
    if not result:
        return Result(error="Отчета не существует")

    return Result(value=result)

