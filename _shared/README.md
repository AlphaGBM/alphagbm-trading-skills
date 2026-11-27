# Shared protocols

共享证据、归因、记录、隐私和安全协议的编辑源。技能使用的协议通过 `python3 scripts/build_packages.py` 生成到各自的 `references/shared/`，安装单个技能不依赖包外目录。只编辑本目录源文件；CI 检查包内副本与源一致，避免规则漂移。
