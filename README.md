# 时光屋 · TimeHouse

一款用于日常锻炼与饮食记录的 Android 应用。安排训练、查看动作演示、跟随计时完成练习，再把训练与餐食记录留在一起。基础训练和记录功能可离线使用，AI 辅助按需开启。

[下载 Android 安装包](https://github.com/charlotteamian/TimeHouse/releases/download/latest-build/timehouse-debug.apk) · [查看版本](https://github.com/charlotteamian/TimeHouse/releases/tag/latest-build) · [反馈问题](https://github.com/charlotteamian/TimeHouse/issues)

## 主要功能

- **训练安排**：结合可用器械、训练时长、强度与伤痛设置安排课程，支持周期计划和训练日历。
- **动作跟练**：查看中文动作说明与离线动画，使用计次、计时、休息倒计时和语音提示完成训练，支持暂停与继续。
- **自定义动作组**：保存常用训练组合，设置组数、次数、时长、休息与重量备注，支持顺序训练和多轮循环。
- **训练记录**：回顾训练用时、实际完成的动作与组数，补充感受和训练心得。
- **饮食记录**：记录每日餐食，管理菜谱与快捷餐，查看能量和营养摄入估算。
- **手表数据**：通过 Health Connect 读取已授权的心率、热量、步数与距离，并关联到训练记录。此功能需要 Android 14 及以上，以及已向 Health Connect 同步数据的手表配套应用。

## 下载与使用

支持 **Android 9 及以上**。

1. [下载 APK](https://github.com/charlotteamian/TimeHouse/releases/download/latest-build/timehouse-debug.apk)，按手机提示安装；如系统询问，请允许当前下载来源安装应用。
2. 打开应用，在设置中选择可用器械与训练偏好。
3. 从「今天」开始一次训练，或创建自己的动作组；在「记录」回顾训练，在「吃什么」管理饮食。

后续可在 **设置 → 应用更新 → 检查更新** 中下载新版，并按系统提示完成安装。下载和更新无需登录 GitHub。

## 数据与可选 AI

训练记录和菜谱保存在本机，可在设置中导出 JSON 备份，并从备份文件导入。

AI 辅助需要自行配置所选服务的 API 密钥，可用于训练推荐、餐食估算和菜谱整理等功能。使用时，相关文字、图片和上下文会发送至所配置的第三方服务。关闭 AI 后，仍可使用本地训练、动作库、记录和内置食谱。

## 反馈与素材说明

欢迎通过 [Issues](https://github.com/charlotteamian/TimeHouse/issues) 反馈问题或建议。

第三方数据与素材来源见 [第三方声明](THIRD_PARTY_NOTICES.md)。
