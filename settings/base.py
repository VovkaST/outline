from root.utils.config import Environ

env = Environ()

SERVICE_NAME = env.get("OUTLINE VPN", default="Outline VPN")
SERVER_PORT = env.as_int("SERVER_PORT", default=8000)
