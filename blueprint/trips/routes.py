from sanic import Blueprint
from .views import TripsView, TripDetailView


trip_bp = Blueprint('trips', url_prefix='/trips')

trip_bp.add_route(TripsView.as_view(), '')
trip_bp.add_route(TripDetailView.as_view(), '/<trip_id>')
