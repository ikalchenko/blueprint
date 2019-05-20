from sanic import Blueprint
from .views import TasksView, TaskDetailView

task_bp = Blueprint('tasks', url_prefix='/trips/<trip_id>/tasks')

task_bp.add_route(TasksView.as_view(), '')
task_bp.add_route(TaskDetailView.as_view(), '/<task_id>')
