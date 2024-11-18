from os import path
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    current_app,
    abort,
)
from ..auth import auth_decorator
from .model import create_report, view_report, get_report_config

module_path = path.dirname(path.abspath(__file__))
reports_blueprint = Blueprint(
    "reports_bp", __name__, template_folder=path.join(module_path, "web")
)


def render_report_type_menu(view: bool):
    reports = [(i[0], i[1].get("friendly_name")) for i in current_app.config['REPORTS'].items()]
    return render_template("report_type_menu.html", reports=reports, view=view)


@reports_blueprint.route('/')
def index():
    return render_template('repindex.html')


@reports_blueprint.route('/create', methods=["GET", "POST"])
@auth_decorator(lambda: url_for("reports_bp.index"))
def create():
    if request.method == 'GET':
        return render_report_type_menu(view=False)
    
    elif request.method == 'POST':
        report_type = request.form.get('report_type')
        config_result = get_report_config(report_type)
        if config_result.is_err():
            return abort(400)
        
        if 'field_values' not in request.form:
            return render_template(
                "report_form.html",
                    fields=config_result.value['fields'],
                report_type=report_type,
                friendly_name=config_result.value['friendly_name']
            )
        
        result = create_report(report_type, request.form)
        if result.is_err():
            return render_template(
                "generic_message.html",
                link=url_for('reports_bp.index'),
                message=result.error
            )
        return render_template(
            "generic_message.html",
            message="Отчёт успешно создан",
            link=url_for('reports_bp.index')
        )


@reports_blueprint.route('/view', methods=['GET', 'POST'])
@auth_decorator(lambda: url_for("reports_bp.index"))
def view():
    if request.method == 'GET':
        return render_report_type_menu(view=True)
    
    elif request.method == 'POST':
        report_type = request.form.get('report_type')
        config_result = get_report_config(report_type)
        if config_result.is_err():
            return abort(400)
        
        if 'field_values' not in request.form:
            return render_template(
                "report_form.html",
                fields=config_result.value['fields'],
                report_type=report_type,
                friendly_name=config_result.value['friendly_name'],
                view=True
            )
        
        result = view_report(report_type, request.form)
        if result.is_err():
            return render_template(
                "generic_message.html",
                link=request.url_rule,
                message=result.error
            )
        return render_template(
            "generic_table.html",
            columns=result.value[0].keys(),
            rows=[i.values() for i in result.value],
            title="Отчет"
        )

