"""MaicLaude 配置模型。"""

from typing import Any, ClassVar, Dict, List

from maibot_sdk import Field, PluginConfigBase


def _ui_extra(
    label: str,
    hint: str,
    order: int,
    *,
    placeholder: str = "",
    input_type: str = "",
    disabled: bool = False,
    hidden: bool = False,
    step: float | int | None = None,
) -> Dict[str, Any]:
    """构造 WebUI 配置项中文显示信息。"""

    extra: Dict[str, Any] = {"label": label, "hint": hint, "order": order}
    if placeholder:
        extra["placeholder"] = placeholder
    if input_type:
        extra["input_type"] = input_type
    if disabled:
        extra["disabled"] = True
    if hidden:
        extra["hidden"] = True
    if step is not None:
        extra["step"] = step
    return extra


class PluginSectionConfig(PluginConfigBase):
    """插件基础配置。"""

    __ui_label__: ClassVar[str] = "基础设置"
    __ui_icon__: ClassVar[str] = "bot"
    __ui_order__: ClassVar[int] = 0

    config_version: str = Field(
        default="1.0.0",
        description="配置版本号。",
        json_schema_extra=_ui_extra("配置版本", "当前配置文件结构版本，通常不需要手动修改。", 0, disabled=True),
    )
    enabled: bool = Field(
        default=True,
        description="是否启用插件。",
        json_schema_extra=_ui_extra("启用插件", "关闭后不会处理 /claude 命令。", 1),
    )


class ServerConfig(PluginConfigBase):
    """远程服务配置。"""

    __ui_label__: ClassVar[str] = "远程服务"
    __ui_icon__: ClassVar[str] = "server"
    __ui_order__: ClassVar[int] = 3

    base_url: str = Field(
        default="",
        description="远程 Ubuntu Agent 服务地址。",
        json_schema_extra=_ui_extra("服务地址", "remote 执行模式下的 HTTP Agent 根地址，例如 https://agent.example.com。", 0),
    )
    api_token: str = Field(
        default="",
        description="远程服务鉴权 token。",
        json_schema_extra=_ui_extra("鉴权 Token", "调用远程服务时使用的 Bearer token。", 1, input_type="password"),
    )
    require_api_token: bool = Field(
        default=True,
        description="是否要求配置远程服务 token。",
        json_schema_extra=_ui_extra("要求 Token", "开启后，remote 模式必须填写 api_token 才能创建任务。", 2),
    )
    create_path: str = Field(
        default="/v1/tasks",
        description="创建任务接口路径。",
        json_schema_extra=_ui_extra("创建任务路径", "远程 Agent 创建任务的 HTTP 路径。", 3),
    )
    status_path_template: str = Field(
        default="/v1/tasks/{task_id}",
        description="查询任务接口路径模板。",
        json_schema_extra=_ui_extra("查询任务路径", "远程 Agent 查询任务状态的路径模板，必须包含 {task_id}。", 4),
    )
    cancel_path_template: str = Field(
        default="/v1/tasks/{task_id}/cancel",
        description="取消任务接口路径模板。",
        json_schema_extra=_ui_extra("取消任务路径", "远程 Agent 取消任务的路径模板，必须包含 {task_id}。", 5),
    )
    request_timeout_seconds: float = Field(
        default=20.0,
        description="HTTP 请求超时秒数。",
        json_schema_extra=_ui_extra("请求超时", "调用远程 Agent 接口的超时时间，单位秒。", 6, step=1),
    )
    verify_tls: bool = Field(
        default=True,
        description="是否校验 HTTPS 证书。",
        json_schema_extra=_ui_extra("校验 TLS 证书", "使用 HTTPS 远程服务时是否校验证书。生产环境建议保持开启。", 7),
    )


class PermissionConfig(PluginConfigBase):
    """触发权限配置。"""

    __ui_label__: ClassVar[str] = "权限"
    __ui_icon__: ClassVar[str] = "shield"
    __ui_order__: ClassVar[int] = 4

    # allow_all_users 是用户维度的总开关。开启后默认所有用户能用；
    # 但 user_list_mode=blacklist 时，trigger_users 里的用户仍会被拦截。
    # 关闭后必须进入旧 allowed_users 或新 trigger_users 白名单。
    allow_all_users: bool = Field(
        default=False,
        description="是否允许所有用户触发。",
        json_schema_extra=_ui_extra("允许所有用户", "开启后默认所有用户都能触发；黑名单模式下 trigger_users 仍会拦截指定用户。", 0),
    )
    allowed_users: List[str] = Field(
        default_factory=list,
        description="允许触发的用户，推荐格式 qq:用户ID。",
        json_schema_extra=_ui_extra("旧版用户白名单", "兼容旧配置。新配置建议使用 user_list_mode 和 trigger_users。", 1, placeholder="qq:123456"),
    )
    user_list_mode: str = Field(
        default="whitelist",
        description="用户列表模式：whitelist 或 blacklist。",
        json_schema_extra=_ui_extra("用户名单模式", "whitelist 只允许名单内用户；blacklist 拦截名单内用户。", 2, placeholder="whitelist / blacklist"),
    )
    trigger_users: List[str] = Field(
        default_factory=list,
        description="用户黑白名单，推荐格式 qq:用户ID。",
        json_schema_extra=_ui_extra("用户黑白名单", "配合用户名单模式使用。推荐写成 qq:用户ID，也兼容只写用户 ID。", 3, placeholder="qq:123456"),
    )
    admin_users: List[str] = Field(
        default_factory=list,
        description="管理员用户，允许使用高危权限。",
        json_schema_extra=_ui_extra("管理员用户", "允许使用 danger-full-access 等高危本地 Claude Code 权限的用户。", 4, placeholder="qq:123456"),
    )
    allowed_groups: List[str] = Field(
        default_factory=list,
        description="允许触发的群号、qq:群号 或 stream_id。",
        json_schema_extra=_ui_extra("旧版聊天白名单", "兼容旧配置。新配置建议使用 chat_list_mode 和 trigger_chats。", 5, placeholder="qq:群号"),
    )
    # “聊天流”是 MaiBot 对会话来源的抽象，可能是群、私聊或 adapter 生成的 stream_id。
    # 用户权限和聊天流权限同时生效，两边都通过才允许触发。
    chat_list_mode: str = Field(
        default="whitelist",
        description="聊天流列表模式：whitelist 或 blacklist。",
        json_schema_extra=_ui_extra("聊天流名单模式", "whitelist 只允许名单内聊天流；blacklist 拦截名单内聊天流。", 6, placeholder="whitelist / blacklist"),
    )
    trigger_chats: List[str] = Field(
        default_factory=list,
        description="聊天流黑白名单，可写群号、qq:群号 或 stream_id。",
        json_schema_extra=_ui_extra("聊天流黑白名单", "触发 /claude 的会话来源名单，可写群号、qq:群号 或 stream_id。", 7, placeholder="qq:群号"),
    )
    reject_temporary_private_chat: bool = Field(
        default=True,
        description="是否拒绝 QQ 群临时私聊触发。",
        json_schema_extra=_ui_extra("拒绝群临时私聊", "群临时会话在部分 QQ 适配器下路由不稳定，建议保持开启。", 8),
    )


class TaskConfig(PluginConfigBase):
    """任务配置。"""

    __ui_label__: ClassVar[str] = "任务"
    __ui_icon__: ClassVar[str] = "terminal"
    __ui_order__: ClassVar[int] = 5

    command_prefix: str = Field(
        default="/claude",
        description="帮助文本默认展示的主命令前缀。",
        json_schema_extra=_ui_extra("命令前缀", "帮助文本里默认展示的主命令。实际命令固定支持 /claude。", 0),
    )
    execution_mode: str = Field(
        default="local",
        description="执行模式：local 或 remote。",
        json_schema_extra=_ui_extra("执行模式", "local 直接调用本机 Claude Code CLI；remote 调用远程 HTTP Agent。", 1, placeholder="local / remote"),
    )
    enable_cancel: bool = Field(
        default=True,
        description="是否允许取消远程任务。",
        json_schema_extra=_ui_extra("允许取消任务", "是否允许用户使用 cancel 命令取消任务。", 2),
    )
    task_type: str = Field(
        default="claude_code_cli",
        description="提交给远程服务的任务类型。",
        json_schema_extra=_ui_extra("远程任务类型", "remote 模式提交给 HTTP Agent 的任务类型。", 3),
    )
    max_running_tasks_per_stream: int = Field(
        default=1,
        description="单个聊天流同时运行的最大任务数。",
        json_schema_extra=_ui_extra("单聊天并发数", "同一个群聊/私聊同时运行的最大任务数。", 4),
    )
    max_running_tasks_per_user: int = Field(
        default=1,
        description="单个用户同时运行的最大任务数。",
        json_schema_extra=_ui_extra("单用户并发数", "同一个用户同时运行的最大任务数。", 5),
    )
    poll_interval_seconds: float = Field(
        default=5.0,
        description="轮询远程任务状态间隔。",
        json_schema_extra=_ui_extra("轮询间隔", "remote 模式查询任务状态的间隔，单位秒。", 6, step=1),
    )
    max_watch_seconds: float = Field(
        default=3600.0,
        description="单个任务最长跟踪时间。",
        json_schema_extra=_ui_extra("最长跟踪时间", "超过该时间后插件停止等待任务结果，单位秒。", 7, step=60),
    )
    resumable_task_ttl_hours: float = Field(
        default=24.0,
        description="普通 task 可继续对话的保留小时数。",
        json_schema_extra=_ui_extra("任务保留时间", "普通 task 可通过 resume 继续对话的保留时间，单位小时。", 8, step=1),
    )
    require_session_confirm: bool = Field(
        default=True,
        description="把 task 转为 session 时是否要求二次确认。",
        json_schema_extra=_ui_extra("Session 二次确认", "把普通 task 转为长期 session 前是否要求用户确认。", 9),
    )
    auto_cleanup_task_records: bool = Field(
        default=True,
        description="启动时是否自动清理过期普通 task 记录。",
        json_schema_extra=_ui_extra("启动清理任务记录", "MaiBot 启动时是否自动清理过期的普通 task 记录。", 10),
    )
    auto_cleanup_task_workspaces: bool = Field(
        default=False,
        description="自动清理过期 task 记录时是否同时删除 task 目录和文件。",
        json_schema_extra=_ui_extra("同时删除任务目录", "清理过期 task 记录时是否删除对应 workspace、产物和日志。请谨慎开启。", 11),
    )
    enable_periodic_cleanup: bool = Field(
        default=False,
        description="是否启用后台定时清理。",
        json_schema_extra=_ui_extra("启用定时清理", "长时间不重启 MaiBot 时可开启，按间隔清理过期任务和输入材料。", 12),
    )
    periodic_cleanup_interval_minutes: float = Field(
        default=60.0,
        description="后台定时清理间隔分钟数。",
        json_schema_extra=_ui_extra("定时清理间隔", "后台定时清理的执行间隔，单位分钟。", 13, step=5),
    )


class LocalClaudeConfig(PluginConfigBase):
    """本机 Claude Code CLI 配置。"""

    __ui_label__: ClassVar[str] = "本地 Claude Code"
    __ui_icon__: ClassVar[str] = "terminal"
    __ui_order__: ClassVar[int] = 6

    claude_binary: str = Field(
        default="claude",
        description="Claude Code CLI 可执行文件名或绝对路径。",
        json_schema_extra=_ui_extra("Claude Code 可执行文件", "Claude Code CLI 命令名或绝对路径，例如 claude。", 0),
    )
    work_root: str = Field(
        default="data/tasks",
        description="本地任务根目录；相对路径按插件目录解析。",
        json_schema_extra=_ui_extra("任务根目录", "本地任务、workspace、输入材料和产物记录的根目录。相对路径按插件目录解析。", 1),
    )
    model: str = Field(
        default="",
        description="可选模型名（alias 或完整 ID）。",
        json_schema_extra=_ui_extra("模型名", "传给 Claude Code 的 --model。留空使用 Claude Code 默认配置。alias: sonnet, opus, haiku, fable", 2),
    )
    max_turns: int = Field(
        default=20,
        description="Claude Code 最大 agentic turns 数。",
        json_schema_extra=_ui_extra("最大 Turns", "传给 Claude Code 的 --max-turns。0 表示不限制。", 3, step=1),
    )
    verbose: bool = Field(
        default=True,
        description="是否启用 --verbose 模式。",
        json_schema_extra=_ui_extra("详细输出", "传给 Claude Code 的 --verbose。开启后配合 stream-json 可提取更详细的进度。", 4),
    )
    extra_args: List[str] = Field(
        default_factory=list,
        description="额外传给 claude -p 的参数。",
        json_schema_extra=_ui_extra("额外参数", "追加传给 claude 的参数。注意不要传 --dangerously-skip-permissions、--output-format 等插件管理的 flag。", 5),
    )
    pass_env_vars: List[str] = Field(
        default_factory=list,
        description="额外传给 Claude Code 子进程的环境变量名；这些变量可能被 Claude Code、MCP 或 skill 读取。",
        json_schema_extra=_ui_extra("传递环境变量", "默认只传最小运行环境。只有确认需要且能接受泄露风险时，才把 API key/token 变量（如 ANTHROPIC_API_KEY）写在这里。", 6, placeholder="ANTHROPIC_API_KEY"),
    )
    process_timeout_seconds: float = Field(
        default=3600.0,
        description="本地 Claude Code 任务运行超时。",
        json_schema_extra=_ui_extra("进程超时", "本地 Claude Code 子进程最长运行时间，单位秒。", 7, step=60),
    )
    artifact_globs: List[str] = Field(
        default_factory=lambda: ["artifacts/*", "*.docx", "*.pdf", "*.md", "*.zip", "*.xlsx", "*.pptx"],
        description="任务 workspace 内产物匹配规则。",
        json_schema_extra=_ui_extra("产物匹配规则", "任务结束后在 workspace 内扫描这些 glob，匹配到的文件会作为产物回传。", 8, placeholder="artifacts/*"),
    )


class ProgressConfig(PluginConfigBase):
    """进度转发配置。"""

    __ui_label__: ClassVar[str] = "进度"
    __ui_icon__: ClassVar[str] = "activity"
    __ui_order__: ClassVar[int] = 7

    forward_progress: bool = Field(
        default=True,
        description="是否把运行进度转发到 QQ。",
        json_schema_extra=_ui_extra("转发运行进度", "是否把 Claude Code CLI 的阶段性进度发送回 QQ。", 0),
    )
    min_send_interval_seconds: float = Field(
        default=5.0,
        description="进度消息最小发送间隔。",
        json_schema_extra=_ui_extra("进度发送间隔", "两次进度消息之间的最小间隔，单位秒。", 1, step=1),
    )
    max_progress_items_per_message: int = Field(
        default=5,
        description="每次最多合并多少条进度。",
        json_schema_extra=_ui_extra("单条消息进度数", "每次进度消息最多合并多少条 Claude Code 进度。", 2),
    )
    max_progress_item_chars: int = Field(
        default=300,
        description="单条进度最大字符数。",
        json_schema_extra=_ui_extra("单条进度长度", "每条进度文本的最大字符数，超出会截断。", 3),
    )
    max_summary_chars: int = Field(
        default=1800,
        description="最终摘要最大字符数。",
        json_schema_extra=_ui_extra("最终摘要长度", "最终结果摘要的最大字符数，超出会截断。", 4),
    )
    # 私聊进度依赖 QQ 适配器公开的 NapCat 兼容 send_private_msg API。
    # QQ 侧通常要求用户先主动私聊过机器人，否则可能发送失败。
    enable_private_progress: bool = Field(
        default=False,
        description="是否允许用户用参数请求私聊接收阶段性进度。",
        json_schema_extra=_ui_extra("允许私聊进度", "允许用户用 --dm 或 --private-progress 请求阶段性进度走私聊。", 5),
    )
    private_progress_trigger_args: List[str] = Field(
        default_factory=lambda: ["--dm", "--private-progress"],
        description="触发私聊进度的命令参数。",
        json_schema_extra=_ui_extra("私聊进度参数", "用户在 /claude 命令中添加这些参数时，会尝试私聊发送阶段性进度。", 6, placeholder="--dm"),
    )
    private_progress_fallback_to_origin: bool = Field(
        default=True,
        description="私聊进度发送失败时是否回退到原聊天流。",
        json_schema_extra=_ui_extra("私聊失败回退", "私聊发送失败时，是否把进度改发回原群聊/私聊。", 7),
    )
    private_progress_send_task_created: bool = Field(
        default=False,
        description="使用私聊进度时是否把任务创建提示也私聊发送。",
        json_schema_extra=_ui_extra("创建提示也私聊", "开启后，使用 --dm 时任务创建提示也发私聊。通常建议关闭，方便群里看到 task_id。", 8),
    )
    private_progress_send_artifacts: bool = Field(
        default=False,
        description="使用私聊进度时是否把最终结果和产物也私聊发送。",
        json_schema_extra=_ui_extra("最终结果也私聊", "开启后，使用 --dm 时最终摘要和产物也尝试私聊发送。", 9),
    )


class ArtifactConfig(PluginConfigBase):
    """产物回传配置。"""

    __ui_label__: ClassVar[str] = "产物"
    __ui_icon__: ClassVar[str] = "file-text"
    __ui_order__: ClassVar[int] = 8

    send_artifact_links: bool = Field(
        default=True,
        description="完成时是否发送产物列表或下载链接。",
        json_schema_extra=_ui_extra("发送产物列表", "任务完成时是否发送生成文件的名称、大小或下载信息。", 0),
    )
    try_custom_file_message: bool = Field(
        default=False,
        description="是否尝试用 send.custom 发送文件消息。",
        json_schema_extra=_ui_extra("尝试自定义文件消息", "早期兼容路径。只有当前适配器支持对应 custom 消息类型时才会成功。", 1),
    )
    custom_file_message_type: str = Field(
        default="file",
        description="自定义文件消息类型。",
        json_schema_extra=_ui_extra("自定义消息类型", "send.custom 使用的消息类型，不同适配器可能不同。", 2),
    )


class NapCatConfig(PluginConfigBase):
    """NapCat Adapter API 配置。"""

    __ui_label__: ClassVar[str] = "NapCat"
    __ui_icon__: ClassVar[str] = "upload"
    __ui_order__: ClassVar[int] = 1

    enabled: bool = Field(
        default=False,
        description="是否使用 NapCat Adapter API；与 SnowLuma 二选一，不会作为 SnowLuma 兜底。",
        json_schema_extra=_ui_extra("启用 NapCat 能力", "开启后使用 NapCat Adapter API 做文件直传、私聊进度和 QQ 文件信息补全。不要和 SnowLuma 同时开启。", 0),
    )
    upload_file: bool = Field(
        default=True,
        description="调用 upload_*_file 时是否执行真实上传。",
        json_schema_extra=_ui_extra("执行真实上传", "关闭后仍走调用路径，但不要求 NapCat 真正上传文件。一般保持开启。", 1),
    )
    max_file_size_mb: float = Field(
        default=100.0,
        description="单个产物最大上传大小，0 表示不限制。",
        json_schema_extra=_ui_extra("最大上传大小", "通过 NapCat 直传的单个产物大小限制，单位 MB；0 表示不限制。", 2, step=1),
    )


class SnowLumaConfig(PluginConfigBase):
    """SnowLuma Adapter 兼容配置。"""

    __ui_label__: ClassVar[str] = "SnowLuma"
    __ui_icon__: ClassVar[str] = "snowflake"
    __ui_order__: ClassVar[int] = 2

    enabled: bool = Field(
        default=False,
        description="是否使用 SnowLuma Adapter；与 NapCat 二选一，不会调用 NapCat 兜底。",
        json_schema_extra=_ui_extra("启用 SnowLuma 能力", "开启后只使用 SnowLuma 适配器公开的 NapCat 兼容 API，不会调用 NapCat 兜底。不要和 NapCat 同时开启。", 0),
    )
    send_artifacts_as_file_segments: bool = Field(
        default=True,
        description="通过 SnowLuma 兼容发送 API 发送 OneBot file 段回传产物；失败时不改用 NapCat。",
        json_schema_extra=_ui_extra("用 file 段回传产物", "开启后通过 SnowLuma 的 send_group_msg/send_private_msg 发送 OneBot file 段；失败时只报告错误，不改用 NapCat。", 1),
    )
    max_file_size_mb: float = Field(
        default=100.0,
        description="SnowLuma file 段单个产物最大大小，0 表示不限制。",
        json_schema_extra=_ui_extra("file 段大小限制", "通过 SnowLuma file 段回传的单个产物大小限制，单位 MB；0 表示不限制。", 2, step=1),
    )


class InputFileConfig(PluginConfigBase):
    """用户输入文件配置。"""

    __ui_label__: ClassVar[str] = "输入文件"
    __ui_icon__: ClassVar[str] = "paperclip"
    __ui_order__: ClassVar[int] = 9

    enable_reply_file: bool = Field(
        default=True,
        description="是否允许回复 QQ 文件消息创建带材料的 Claude Code 任务。",
        json_schema_extra=_ui_extra("允许回复文件作为输入", "用户回复 QQ 文件消息并发送 /claude 时，插件会把文件导入 workspace/input。", 0),
    )
    input_dir_name: str = Field(
        default="input",
        description="输入材料放入 workspace 下的目录名。",
        json_schema_extra=_ui_extra("输入目录名", "输入材料在 Claude Code workspace 下的目录名。", 1),
    )
    max_files_per_task: int = Field(
        default=5,
        description="单个任务最多导入多少个文件。",
        json_schema_extra=_ui_extra("最多导入文件数", "一个 /claude 任务最多导入多少个被回复或附带的文件。", 2),
    )
    max_file_size_mb: float = Field(
        default=100.0,
        description="单个输入文件最大大小，0 表示不限制。",
        json_schema_extra=_ui_extra("输入文件大小限制", "单个输入材料的大小限制，单位 MB；0 表示不限制。", 3, step=1),
    )
    allow_url_download: bool = Field(
        default=True,
        description="是否允许从 QQ 文件消息中的 HTTP URL 下载输入文件。",
        json_schema_extra=_ui_extra("允许 URL 下载", "允许插件从 QQ 文件消息里的 http/https URL 下载输入材料。", 4),
    )
    download_timeout_seconds: float = Field(
        default=120.0,
        description="输入文件 URL 下载超时秒数。",
        json_schema_extra=_ui_extra("下载超时", "从 QQ 文件 URL 下载输入材料的超时时间，单位秒。", 5, step=10),
    )
    allowed_local_roots: List[str] = Field(
        default_factory=list,
        description="允许复制的本地文件根目录，空列表表示禁止复制本地路径。",
        json_schema_extra=_ui_extra("允许的本地根目录", "允许插件复制服务器本地文件的根目录。空列表表示禁止读取本地路径，日常建议保持为空。", 6),
    )
    auto_cleanup_input_files: bool = Field(
        default=True,
        description="启动时是否自动清理过期输入材料。",
        json_schema_extra=_ui_extra("自动清理输入材料", "启动或定时清理时，是否删除超过 TTL 的 workspace/input 输入材料。", 7),
    )
    input_file_ttl_hours: float = Field(
        default=24.0,
        description="输入材料保留小时数，0 表示不自动清理。",
        json_schema_extra=_ui_extra("输入材料保留时间", "输入材料在 workspace/input 中保留的时间，单位小时；0 表示不自动清理。", 8, step=1),
    )


class RemoteClaudeCodeAgentConfig(PluginConfigBase):
    """远程 Claude Code Agent 插件配置。"""

    plugin: PluginSectionConfig = Field(
        default_factory=PluginSectionConfig,
        description="插件基础配置。",
        json_schema_extra=_ui_extra("基础设置", "插件启用状态和配置版本。", 0),
    )
    napcat: NapCatConfig = Field(
        default_factory=NapCatConfig,
        description="NapCat Adapter API 配置。",
        json_schema_extra=_ui_extra("NapCat", "NapCat Adapter API 增强能力。", 1),
    )
    snowluma: SnowLumaConfig = Field(
        default_factory=SnowLumaConfig,
        description="SnowLuma Adapter 兼容配置。",
        json_schema_extra=_ui_extra("SnowLuma", "SnowLuma Adapter 的 NapCat 兼容 API 增强能力。", 2),
    )
    server: ServerConfig = Field(
        default_factory=ServerConfig,
        description="远程服务配置。",
        json_schema_extra=_ui_extra("远程服务", "remote 执行模式使用的 HTTP Agent 配置。", 3),
    )
    permission: PermissionConfig = Field(
        default_factory=PermissionConfig,
        description="触发权限配置。",
        json_schema_extra=_ui_extra("权限", "控制哪些用户和聊天流可以触发 /claude。", 4),
    )
    task: TaskConfig = Field(
        default_factory=TaskConfig,
        description="任务配置。",
        json_schema_extra=_ui_extra("任务", "任务创建、并发、保留和清理策略。", 5),
    )
    local_claude: LocalClaudeConfig = Field(
        default_factory=LocalClaudeConfig,
        description="本机 Claude Code CLI 配置。",
        json_schema_extra=_ui_extra("本地 Claude Code", "local 执行模式下调用 Claude Code CLI 的配置。", 6),
    )
    progress: ProgressConfig = Field(
        default_factory=ProgressConfig,
        description="进度转发配置。",
        json_schema_extra=_ui_extra("进度", "运行进度、最终摘要和私聊进度配置。", 7),
    )
    artifact: ArtifactConfig = Field(
        default_factory=ArtifactConfig,
        description="产物回传配置。",
        json_schema_extra=_ui_extra("产物", "任务完成后的产物列表、下载链接或文件消息回传配置。", 8),
    )
    input_file: InputFileConfig = Field(
        default_factory=InputFileConfig,
        description="输入文件配置。",
        json_schema_extra=_ui_extra("输入文件", "回复 QQ 文件作为 Claude Code 输入材料的配置。", 9),
    )


