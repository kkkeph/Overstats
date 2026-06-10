from __future__ import annotations

import json
import os


def _env(key: str, default: str = "") -> str:
    """读取环境变量，不存在时返回默认值。"""
    return os.getenv(key, default)


def _env_json(key: str, default: str = "[]") -> list:
    """读取 JSON 格式的环境变量（用于列表配置）。"""
    raw = os.getenv(key, default)
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return []


# ======================= Core Service ====================== #
API_HOST = "127.0.0.1"
API_PORT = 18080
USE_STREAM_RESPONSE = True
ENABLE_DATABASE_WRITE = True

# ======================= Dashen Upstream ====================== #
# Configure at least one account.
# 优先使用环境变量 OVERSTATS_DASHEN_ACCOUNTS_JSON（JSON 数组），
# 为空时使用下面的默认值。
DASHEN_ACCOUNTS = _env_json(
    "OVERSTATS_DASHEN_ACCOUNTS_JSON",
    json.dumps([
        {
            "name": "account-1",
            "role_id": 223612789,
            "token": "f3b144deaefb09c20fcff103a6394631",
        },
        # {
        #     "name": "account-2",
        #     "role_id": 987654321,
        #     "token": "replace-with-your-token",
        # },
    ]),
)

DASHEN_DTS = 2026
DASHEN_SERVER = 1
DASHEN_ACCOUNT_MAX_REQUESTS_PER_SECOND = 5
DASHEN_ACCOUNT_RATE_LIMIT_WINDOW_SECONDS = 1.0
DASHEN_CLIENT_TYPE = "60"
DASHEN_ORIGIN = "https://act.ds.163.com"
DASHEN_REFERER = "https://act.ds.163.com/"
DASHEN_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 "
    "app/df_client dfVersion/100111"
)
DASHEN_ACCOUNT_FAILURE_COOLDOWN_SECONDS = 60
DASHEN_MAX_CONCURRENT_REQUESTS = 2
# Main v2 Dashen endpoints accept at most account-pool-size * 4 requests
# (active + queued) by default. Extra requests receive HTTP 429.
DASHEN_MAX_ACCEPTED_REQUESTS = max(len(DASHEN_ACCOUNTS) * 4, 1)

# Optional proxy settings.
DASHEN_INTERNATIONAL_PROXY = ""
DASHEN_NETEASE_PROXIES = [
    None,
    # "http://your-netease-proxy:port",
]

# OW esports PandaScore API key.
#如何获取ow赛事的apikey:访问https://app.pandascore.co/dashboard/main，注册并生成api key，每小时1000次免费调用
OW_ESPORTS_API_KEY = _env("OVERSTATS_OW_ESPORTS_API_KEY", "")

# Optional external OW guess asset pack root.
# 仅存放本地图片/音频等大资源，默认放在 Overstats 项目目录外的相邻文件夹。
# Default location: <repo>/ow_guess_assets (gitignored, optional install).
OW_GUESS_ASSET_ROOT = "ow_guess_assets"

# ======================= OW Hero Leaderboard ====================== #
OW_HERO_LEADERBOARD_CN_SEASON = 2

# ======================= Match Analysis ====================== #
# OpenAI-compatible base URL, for example:
# - https://api.openai.com/v1
# - https://api.deepseek.com/v1
# - https://generativelanguage.googleapis.com/v1beta/openai
# You can also provide the full /chat/completions endpoint directly.
ANALYSIS_BASE_URL = _env("OVERSTATS_ANALYSIS_BASE_URL", "https://api.moonshot.cn/v1/chat/completions")
ANALYSIS_API_KEY = _env("OVERSTATS_ANALYSIS_API_KEY", "sk-Cij9yfBISs1C75EdK8ftyPKbzAjpTMEaTg8KjETsy3M3Z3Mc")
# Optional proxy for OpenAI official and Google OpenAI-compatible endpoints.
ANALYSIS_PROXY = ""

# ANALYSIS_GOOGLE_MODEL = "gemini-3.1-flash-lite-preview"
#ANALYSIS_DEEPSEEK_MODEL = "deepseek-chat"
#除谷歌和deepseek以外的模型使用下面配置
ANALYSIS_OPENAI_MODEL = "kimi-k2.6"


# Optional external patch-note fetch proxy.
PATCH_NOTES_USE_INTERNATIONAL_PROXY = False
PATCH_NOTES_INTERNATIONAL_PROXY = ""

# Only put AI persona/tone here.
# Task instructions and the JSON schema remain in service.py.
ANALYSIS_PERSONA_PROMPT = """
【核心原则】
请保持绝对客观中立，拒绝阿谀奉承！不要因为查询指令的是焦点玩家就一味夸奖，如果焦点玩家表现平庸或拉垮请直接批评。

【人格设定】
你的说话人设是科比·布莱恩特，风格包含 [man! what can i say，mamba out] 等 meme。
""".strip()
