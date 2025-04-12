from root.utils.config import Environ

env = Environ()

SERVICE_NAME = env.get("OUTLINE VPN", default="Outline VPN")
SERVER_PORT = env.as_int("SERVER_PORT", default=8000)
SERVER_VERSION = env.get("SERVER_VERSION", default="1.0")
SERVER_DESCRIPTION = env.get("SERVER_DESCRIPTION")
