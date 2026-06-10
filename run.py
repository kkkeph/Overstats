from __future__ import annotations

import os as _os
import sys as _sys

# 确保仓库根目录的父目录在 sys.path 上，使得 `overstats` 包可被发现。
# 适用于 Docker（WORKDIR=/opt/overstats）以及本地开发环境。
# 必须在任何 `from overstats.*` 导入之前执行。
_repo_root = _os.path.dirname(_os.path.abspath(__file__))
_repo_parent = _os.path.dirname(_repo_root)
if _repo_parent not in _sys.path:
    _sys.path.insert(0, _repo_parent)

try:
    from overstats.config import get_api_config
    from overstats.src import create_server
except ModuleNotFoundError:
    from config import get_api_config
    from src import create_server


def main() -> None:
    config = get_api_config()
    server = create_server(config)
    print(
        f"[overstats] serving on http://{config.host}:{config.port} "
        f"(default_stream={config.use_stream_response})"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
