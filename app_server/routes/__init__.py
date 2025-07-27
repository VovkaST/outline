__all__ = [
    "keys_routes",
    "orders_routes",
    "payments_routes",
    "server_routes",
    "subscription_routes",
]

from .keys import routes as keys_routes
from .orders import routes as orders_routes
from .payments import routes as payments_routes
from .server import routes as server_routes
from .subscription import routes as subscription_routes
